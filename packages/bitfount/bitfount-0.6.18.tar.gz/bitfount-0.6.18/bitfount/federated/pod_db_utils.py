"""Utilities for the Pod results database."""
from datetime import datetime
import hashlib
import os.path
from pathlib import Path
from sqlite3 import Connection, Cursor, OperationalError
from typing import List, Optional, Sequence, Union, cast

import numpy as np
import pandas as pd
import pandas._libs.lib as lib

from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
    MultiTableSource,
)
from bitfount.data.datasources.views import DataView
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.types import DataSplit
from bitfount.federated import _get_federated_logger
from bitfount.federated.types import SerializedProtocol
from bitfount.utils.db_connector import PodDbConnector

logger = _get_federated_logger(__name__)

_RESULTS_COLUMN_NAME: str = "results"


# ######## ADAPTED FROM `pandas.io.sql.py` (CAN'T BE IMPORTED) #########

# ---- SQL without SQLAlchemy ---
# sqlite-specific sql strings and handler class
# dictionary used for readability purposes
_SQL_TYPES = {
    "string": "TEXT",
    "floating": "REAL",
    "integer": "INTEGER",
    "datetime": "TIMESTAMP",
    "date": "DATE",
    "time": "TIME",
    "boolean": "INTEGER",
}


def update_pod_db(
    pod_name: str,
    connector: PodDbConnector,
    datasource_name: str,
    datasource: BaseSource,
) -> None:
    """Creates and updates the pod database.

    This is a static database on the pod with the datapoint hashes so we only
    compute them once. For each datapoint row in the datasource, a hash value
    is computed. Then the data from (each table of) the datasource,
    together with the hash value, are written to the database.


    :::caution

    Does not work for multi-table `DatabaseSource`s as we cannot load the data into
    memory.

    :::
    """
    logger.info(f"Updating pod database for {datasource_name}...")
    # To avoid name clashes with tables of the same name in other datasources
    # we need to modify the table names in multi-table to add the datasource name.
    if datasource.multi_table:
        datasource = cast(MultiTableSource, datasource)
        for table in datasource.table_names:
            # if table name is given as an arg to get_data
            # then it will always return a df, so we can cast
            new_data = cast(pd.DataFrame, datasource.get_data(table_name=table)).copy()
            _add_data_to_pod_db(
                connector=connector,
                pod_name=pod_name,
                data=new_data,
                table_name=f"{datasource_name}_{table}",
            )
    # If the datasource is a FileSystemIterableSource,
    elif isinstance(datasource, FileSystemIterableSource):
        _add_file_iterable_datasource_to_db(
            connector=connector,
            pod_name=pod_name,
            datasource=datasource,
            table_name=datasource_name,
        )
    # If there's only one table in the datasource we can just use the datasource
    # name directly.
    else:
        # This works regardless of whether or not the datasource is iterable
        datasource.load_data()
        _add_data_to_pod_db(
            connector=connector,
            pod_name=pod_name,
            data=datasource.data.copy(),
            table_name=datasource_name,
        )


def _sql_type_name(col: pd.Series) -> str:
    """Takes a pandas column and returns the appropriate SQLite dtype."""
    # Infer type of column, while ignoring missing values.
    # Needed for inserting typed data containing NULLs, GH 8778.
    col_type = lib.infer_dtype(col, skipna=True)

    if col_type == "timedelta64":
        logger.warning(
            "the 'timedelta' type is not supported, and will be "
            "written as integer values (ns frequency) to the database.",
        )
        col_type = "integer"

    elif col_type == "datetime64":
        col_type = "datetime"

    elif col_type == "empty":
        col_type = "string"

    elif col_type == "complex":
        raise ValueError("Complex datatypes not supported")

    if col_type not in _SQL_TYPES:
        col_type = "string"

    return _SQL_TYPES[col_type]


#########################################################################


def _add_data_to_pod_db(
    connector: PodDbConnector,
    pod_name: str,
    data: pd.DataFrame,
    table_name: str,
    file_iterable_datasource: bool = False,
) -> None:
    """Adds the data in the provided dataframe to the pod database.

    Args:
        connector: The PodDbConnector object for database connection.
        pod_name: The name of the pod the database is associated with.
        data: Dataframe to be added to the database.
        table-name: The table from the datasource corresponding to the data.

    Raises:
        ValueError: If there are clashing column names in the datasource
            and the pod database.
    """
    con = connector.get_db_connection_from_name(pod_name=pod_name)
    cur = con.cursor()
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{table_name}" ('rowID' INTEGER PRIMARY KEY)"""  # noqa: B950
    )
    con.commit()

    if "datapoint_hash" in data.columns:
        raise ValueError(
            "`datapoint_hash` not supported as column name in the datasource."
        )
    # Placeholder for the datapoint hash
    data["datapoint_hash"] = ""

    # sqlite transforms bool values to int, so we need to make sure that
    # they are the same in the df so the hashes match
    bool_cols = [col for col in data.columns if data[col].dtype == bool]
    # replace bools by their int value, as it will be done by
    # sqlite in the db anyway
    data[bool_cols] *= 1
    # Remove ' from column names
    for col in data.columns:
        if "'" in col:
            col_text = col.replace("'", "`")
            data.rename(columns={col: col_text}, inplace=True)
    # Reindex to make sure all columns are filled otherwise
    # might have mismatches in columns for the FileSystemIterableSource
    # as different files can have different columns filled.
    data = data.reindex(sorted(data.columns), axis=1)
    hashed_list = []
    if not file_iterable_datasource:
        for _, row in data.iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    else:
        # Special case for file iterable datasources.
        # This is because if we reload the pod,
        # and check if records have been changed one by one,
        # the columns are likely to differ between single files.
        # Since we know that these column will always be part
        # of the datasource and good identifiers for the columns,
        # we only hash them instead of all features.
        for _, row in data[["_original_filename", "_last_modified"]].iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    data["datapoint_hash"] = hashed_list
    # read the db data for the datasource
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    existing_data: pd.DataFrame = pd.read_sql_query(
        f'SELECT * FROM "{table_name}"', con  # nosec hardcoded_sql_expressions
    )
    existing_cols_without_index = set(
        sorted(
            [i for i in existing_data.columns if i not in ["rowID", "datapoint_hash"]]
        )
    )
    # check if df is empty or if columns all columns are the same,
    # if not all the hashes will have to be recomputed
    if (
        not existing_data.empty
        and set(sorted(data.columns)) == existing_cols_without_index
    ):
        data = pd.concat(
            [
                data,
                existing_data.drop(
                    columns=["datapoint_hash", "rowID"], errors="ignore"
                ),
            ],
            join="outer",
            ignore_index=True,
        )
        data.drop_duplicates(inplace=True)
    else:
        cur = con.cursor()
        # replace table if columns are mismatched
        cur.execute(f"DROP TABLE '{table_name}'")
        cur.execute(f"""CREATE TABLE "{table_name}" ('rowID' INTEGER PRIMARY KEY)""")
        for col in data.columns:
            try:
                cur.execute(
                    f"ALTER TABLE '{table_name}' ADD COLUMN '{col}' {_sql_type_name(data[col])}"  # noqa: B950
                )
            except OperationalError:
                # this can happen due to duplicate column name due to formatting issues
                pass
    data.to_sql(table_name, con=con, if_exists="append", index=False)
    con.close()


def _add_file_iterable_datasource_to_db(
    connector: PodDbConnector,
    pod_name: str,
    datasource: FileSystemIterableSource,
    table_name: str,
) -> None:
    """Adds the data from a FileIterableDatasource to the pod database.

    Args:
        connector: The PodDbConnector object for database connection.
        pod_name: The name of the pod the database is associated with.
        datasource: FileIterableSource to be added to the database.
        table_name: The table from the datasource corresponding to the data.

    """
    reload_db = False
    if len(datasource.file_names) != 0:
        # Steps:
        # 1. See if db exists and if any of the filenames are in the db.
        # 2. If any of the files are in the db, we check the timestamp for
        #   last modified.
        # 3. If current last modified timestamp for any of the files is different from
        #   the one in the database we add all of them to a list, and use get_data
        #   just on those filenames.
        con = connector.get_db_connection_from_name(pod_name=pod_name)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cur.fetchall()]
        if table_name not in tables:
            # Ignoring the security warning because the sql query is trusted and
            # the table is checked that it matches the datasource tables.
            cur.execute(
                f"""CREATE TABLE IF NOT EXISTS "{table_name}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
            )
            con.commit()
        cursor = con.execute(
            f"SELECT * FROM '{table_name}'"  # nosec hardcoded_sql_expressions
        )
        column_list = list(map(lambda x: x[0], cursor.description))

        if len(column_list) == 1:
            # This means only column is the `rowId` and we need
            # to load the whole datasource.
            datasource.load_data()
            _add_data_to_pod_db(
                connector=connector,
                pod_name=pod_name,
                data=datasource.data.copy(),
                table_name=table_name,
                file_iterable_datasource=True,
            )

        else:
            # Check if we need to remove rows from the pod database
            # if files no longer exist in provided location
            db_filenames = pd.read_sql(
                f'SELECT "_original_filename" FROM "{table_name}"',  # nosec hardcoded_sql_expressions # noqa: B950
                con,
            )
            rows_to_remove = [
                fname
                for fname in db_filenames["_original_filename"].tolist()
                if fname not in datasource.file_names
            ]
            if len(rows_to_remove) != 0:
                for fname in rows_to_remove:
                    cur.execute(
                        f"""DELETE FROM '{table_name}' WHERE _original_filename='{fname}';"""  # nosec hardcoded_sql_expressions # noqa: B950
                    )
                    con.commit()

            pod_data = pd.read_sql(
                f'SELECT * FROM "{table_name}"', con  # nosec hardcoded_sql_expressions
            )

            for file in datasource.file_names:
                # if file already in db, check if it has been modified.
                if file in pod_data["_original_filename"].tolist():
                    last_modified = datetime.fromtimestamp(
                        os.path.getmtime(file)
                    ).isoformat()
                    db_last_modified_for_file = (
                        pod_data["_last_modified"]
                        .loc[pod_data["_original_filename"] == file]
                        .values
                    )
                    if len(db_last_modified_for_file) == 1:
                        # check against pd datetime to avoid formatting issues
                        if not pd.to_datetime(
                            db_last_modified_for_file[0]
                        ) == pd.to_datetime(last_modified):
                            # If the `_last_modified` column does not match
                            # we need to reload the file
                            # Get record from filename
                            updated_record = datasource._get_data(file_names=[file])
                            _update_single_record_in_db(
                                updated_record=updated_record,
                                original_record=pod_data.loc[
                                    pod_data["_original_filename"] == file
                                ],
                                table_name=table_name,
                                con=con,
                                cur=cur,
                            )
                    else:
                        # This `should` not happen, but `if` it does, the whole db
                        # needs reloading
                        reload_db = True
                        break
                else:
                    # Get record from filename
                    new_record = datasource._get_data(file_names=[file])
                    # If the filename is not found in the database, it
                    # means it is a new record, so we only need to
                    # add that record to the db.
                    _add_single_record_to_db(
                        new_record=new_record, table_name=table_name, con=con, cur=cur
                    )
        if reload_db is True:
            _add_data_to_pod_db(
                connector=connector,
                pod_name=pod_name,
                data=datasource.data.copy(),
                table_name=table_name,
                file_iterable_datasource=True,
            )
        else:
            con.close()

    else:
        # If there are no files found by the datasource,
        # we need to clear the pod database if it exists
        # and log a warning.
        db_file: Path = (
            Path(f"{pod_name}.sqlite")
            if connector.db_files_location is None
            else connector.db_files_location / pod_name
        )
        if os.path.exists(db_file):
            logger.warning("There is no data in the datasource, clearing pod database.")
            con = connector.get_db_connection_from_name(pod_name=pod_name)
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cur.fetchall()]
            # if datasource found no files, then clean-up the pod database
            if table_name in tables:
                cur.execute(
                    f"""DELETE FROM '{table_name}'"""  # nosec hardcoded_sql_expressions # noqa: B950
                )
                con.commit()
            con.close()
        else:
            logger.warning(
                "There is no data in the datasource, no pod database initialised."
            )


def _add_new_col_to_db(
    column_names: List[str],
    new_column: str,
    record: pd.DataFrame,
    table_name: str,
    cur: Cursor,
) -> None:
    if "'" in new_column:
        col_text = new_column.replace("'", "`")
        # TODO: [BIT-3417] Fix SettingWithCopyWarning
        # May also apply to other places in this module where `inplace=True` is used
        record.rename(columns={new_column: col_text}, inplace=True)
    else:
        col_text = new_column
    # Need to update with new columns if any
    if col_text not in column_names:
        try:
            cur.execute(
                f"ALTER TABLE '{table_name}' ADD COLUMN '{col_text}' {_sql_type_name(record[col_text])}"  # noqa: B950
            )
        except OperationalError:
            # this can happen due to duplicate column name due to formatting issues
            pass


def _add_single_record_to_db(
    new_record: pd.DataFrame, table_name: str, con: Connection, cur: Cursor
) -> None:
    """Adds a single record to the pod database."""
    cursor = con.execute(
        f"SELECT * FROM '{table_name}'"  # nosec hardcoded_sql_expressions
    )
    column_names = list(map(lambda x: x[0], cursor.description))
    bool_cols = [col for col in new_record.columns if new_record[col].dtype == bool]
    # SQLite transforms bool cols to int,so we can update them here as well.
    new_record[bool_cols] *= 1
    # Calculate hash
    new_record["datapoint_hash"] = hashlib.sha256(
        str(new_record[["_original_filename", "_last_modified"]].squeeze()).encode(
            "utf-8"
        )
    ).hexdigest()
    # Remove ' from column names
    for col in new_record.columns:
        _add_new_col_to_db(
            column_names=column_names,
            new_column=col,
            record=new_record,
            table_name=table_name,
            cur=cur,
        )

    # Append the record to the db.
    new_record.to_sql(table_name, con=con, if_exists="append", index=False)


def _update_single_record_in_db(
    updated_record: pd.DataFrame,
    original_record: pd.DataFrame,
    table_name: str,
    con: Connection,
    cur: Cursor,
) -> None:
    """Updates a single record in the pod_database."""
    # There is a check that the updated record only has
    # one row prior to calling this function.

    # Replace bools by their int value, as it will be done by
    # sqlite in the db anyway
    bool_cols = [
        col for col in updated_record.columns if updated_record[col].dtype == bool
    ]
    updated_record[bool_cols] *= 1
    # Remove ' from column names
    for col in updated_record.columns:
        _add_new_col_to_db(
            column_names=original_record.columns.to_list(),
            new_column=col,
            record=updated_record,
            table_name=table_name,
            cur=cur,
        )

    # Calculate hash
    updated_record["datapoint_hash"] = hashlib.sha256(
        str(updated_record[["_original_filename", "_last_modified"]].squeeze()).encode(
            "utf-8"
        )
    ).hexdigest()
    for col, feature in updated_record.squeeze().items():
        # Note that double quotes need to be used  for `col`
        # below in case column name has spaces (quite common for DICOMs)
        query = f"""UPDATE "{table_name}" SET "{col}"="{str(feature)}" WHERE "rowID"={original_record.squeeze()["rowID"]}"""  # noqa: B950 # nosec
        cur.execute(query)
        con.commit()


def _map_task_to_hash_add_to_db(
    serialized_protocol: SerializedProtocol, task_hash: str, project_db_con: Connection
) -> None:
    """Maps the task hash to the protocol and algorithm used.

    Adds the task to the task database if it is not already present.

    Args:
        serialized_protocol: The serialized protocol used for the task.
        task_hash: The hash of the task.
        project_db_con: The connection to the database.
    """
    algorithm_ = serialized_protocol["algorithm"]
    if not isinstance(algorithm_, Sequence):
        algorithm_ = [algorithm_]
    for algorithm in algorithm_:
        if "model" in algorithm:
            algorithm["model"].pop("schema", None)
            if algorithm["model"]["class_name"] == "BitfountModelReference":
                algorithm["model"].pop("hub", None)

    cur = project_db_con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS "task_definitions" ('index' INTEGER  PRIMARY KEY AUTOINCREMENT  NOT NULL, 'taskhash' TEXT,'protocol' TEXT,'algorithm' TEXT)"""  # noqa: B950
    )
    data = pd.read_sql("SELECT * FROM 'task_definitions' ", project_db_con)
    if task_hash not in list(data["taskhash"]):
        logger.info("Adding task to task database")
        cur.execute(
            """INSERT INTO "task_definitions" ('taskhash',  'protocol', 'algorithm' ) VALUES (?,?,?);""",  # noqa: B950
            (
                task_hash,
                serialized_protocol["class_name"],
                str(algorithm_),
            ),
        )
    else:
        logger.debug("Task already in task database")
    project_db_con.commit()


def _save_results_to_db(
    connector: PodDbConnector,
    project_db_con: Connection,
    datasource: BaseSource,
    results: Union[List[np.ndarray], pd.DataFrame],
    run_on_new_data_only: bool,
    pod_identifier: str,
    show_datapoints_in_results_db: bool,
    task_hash: str,
    query: Optional[str] = None,
    table: Optional[str] = None,
) -> None:
    """Saves the results to the database.

    Args:
        connector: The PodDbConnector object for database connection.
        project_db_con: The connection to the project database.
        datasource: The datasource used for the task.
        results: The results of the task.
        run_on_new_data_only: Whether the task was run on new data only. This is
            used to determine which rows of the data should be saved to the database.
        pod_identifier: The identifier of the pod.
        show_datapoints_in_results_db: Whether to show the datapoints in the results
            database.
        task_hash: The hash of the task.
        table: The table to get pod data from. Defaults to None.
        query: The query to get pod data from SQLDataView. Defaults to None.

    """
    logger.info("Saving results to database")
    task_results: Union[List[str], pd.DataFrame]
    # Ignoring the security warning because the sql query is trusted and
    # the task_hash is calculated at __init__.
    task_data = pd.read_sql(
        f'SELECT * FROM "{task_hash}"',  # nosec hardcoded_sql_expressions
        project_db_con,
    )
    # add results columns to project_db
    project_db_cur = project_db_con.cursor()
    if isinstance(results, pd.DataFrame):
        task_results = results
        results_cols = results.columns.tolist()
        for col in results_cols:
            if col not in task_data.columns:
                project_db_cur.execute(
                    f"ALTER TABLE '{task_hash}' ADD COLUMN '{col}' {_sql_type_name(task_results[col])}"  # noqa: B950
                )
    else:  # if `task_results` is a list
        # Convert results to string
        task_results = [str(item) for item in results]
        # results_cols = [_ResultsColumnName]
        if _RESULTS_COLUMN_NAME not in task_data.columns:
            project_db_cur.execute(
                f"ALTER TABLE '{task_hash}' ADD COLUMN '{_RESULTS_COLUMN_NAME}' TEXT"  # noqa: B950
            )
    project_db_con.commit()
    # Read in existing results from the relevant database table
    pod_db_con = connector.get_db_connection_from_identifier(
        pod_identifier=pod_identifier
    )
    if table is not None:
        # Ignoring the security warning because the sql query is trusted and
        # the table is checked that it matches the datasource tables in
        # `get_pod_db_table_name`, which is how it gets passed to this function.
        pod_data = pd.read_sql(
            f'SELECT * FROM "{table}"', pod_db_con  # nosec hardcoded_sql_expressions
        )
    elif query is not None:
        pod_data = pd.read_sql(query, pod_db_con)
    else:
        pod_db_con.close()
        logger.warning(
            "Either table name or query needs to be passed. "
            "No results saved to the pod database."
        )
        return
    pod_db_con.close()

    # We only care about the test data since we don't log
    # anything in the database for validation or training data
    if datasource._test_idxs is None:
        if not datasource.iterable:
            raise ValueError("Datasource has no test set, cannot save results.")
        else:
            datasource = cast(FileSystemIterableSource, datasource)
            data_splitter = datasource.data_splitter or PercentageSplitter()
            filenames = data_splitter.get_filenames(datasource, DataSplit.TEST)
            run_data = datasource.data.loc[
                datasource.data["_original_filename"].isin(filenames)
            ].reset_index(drop=True)
    else:
        run_data = datasource.data.loc[datasource._test_idxs].reset_index(drop=True)
    # Remove ' from column names
    for col in run_data.columns:
        if "'" in col:
            col_text = col.replace("'", "`")
            run_data.rename(columns={col: col_text}, inplace=True)
    # pd.read_sql does not map all dtypes correctly,
    # so convert all datetime columns appropriately
    datetime_cols = [
        col for col in run_data.columns if run_data[col].dtype == "datetime64[ns]"
    ]
    for col in datetime_cols:
        pod_data[col] = pd.to_datetime(pod_data[col])

    # Add the results to the run_data. Since `run_data` is a dataframe,
    # we need to handle the cases when the task results are a list and
    # a dataframe differently.
    if isinstance(task_results, pd.DataFrame):
        run_data = pd.concat([run_data, task_results], axis=1)
    else:  # if `task_results` is a list
        # mypy_reason: This access is completely fine, the pandas stubs are overzealous
        run_data.loc[:, _RESULTS_COLUMN_NAME] = task_results  # type: ignore[index] # Reason: see comment # noqa: B950

    columns = list(pod_data.columns)
    columns.remove("datapoint_hash")
    file_iterable = False
    if isinstance(datasource, DataView):
        if isinstance(datasource._datasource, FileSystemIterableSource):
            file_iterable = True
    else:
        if isinstance(datasource, FileSystemIterableSource):
            file_iterable = True
    if file_iterable:
        data_w_hash = pd.merge(
            pod_data,
            run_data,
            how="outer",
            left_on=["_original_filename", "_last_modified"],
            right_on=["_original_filename", "_last_modified"],
            indicator=True,
            suffixes=[None, "_x"],
        ).loc[lambda x: x["_merge"] == "both"]
        # Keep track of the columns,  so we can add them to the project db if needed
        if isinstance(results, pd.DataFrame):
            # if results is a dataframe, then we need to save all the results columns
            data_w_hash = data_w_hash[
                columns + ["datapoint_hash"] + results.columns.tolist()
            ]
        else:
            # If `task_results` is a list, then all results will be saved
            # under the column _RESULTS_COLUMN_NAME
            data_w_hash = data_w_hash[
                columns + ["datapoint_hash", _RESULTS_COLUMN_NAME]
            ]
        columns.remove("rowID")
    else:
        # We don't need to merge on the hash, so drop it from the run_data
        if "datapoint_hash" in run_data.columns:
            run_data.drop("datapoint_hash", inplace=True, axis=1)
        if "rowID" in columns:
            columns.remove("rowID")
        # get the datapoint hashes from the pod db
        data_w_hash = pd.merge(
            pod_data,
            run_data,
            how="outer",
            left_on=columns,
            right_on=columns,
            indicator=True,
        ).loc[lambda x: x["_merge"] == "both"]
        # drop the merge indicator column
        data_w_hash.drop("_merge", inplace=True, axis=1)
    if "rowID" in data_w_hash.columns:
        data_w_hash.drop("rowID", inplace=True, axis=1)
    data_w_hash.drop_duplicates(inplace=True, keep="last")

    # If this is the first time the task is run, it will not
    # have all the columns, so we need to make sure they are
    # added. Otherwise, we don't need to worry about the columns
    # as any alterations to them will be classified as a new task
    if len(task_data) == 0 and show_datapoints_in_results_db:
        for col in columns:
            if col not in task_data.columns:
                project_db_cur.execute(
                    f"ALTER TABLE '{task_hash}' ADD COLUMN '{col}' {_sql_type_name(data_w_hash[col])}"  # noqa: B950
                )

    if run_on_new_data_only:
        # do merge and get new datapoints only
        data_w_hash = pd.merge(
            data_w_hash,
            task_data["datapoint_hash"],
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only"]
        data_w_hash = data_w_hash.drop(columns=["rowID", "_merge"], errors="ignore")
        logger.info(
            f"The task was run on {len(data_w_hash)} "
            f"records from the datasource."  # nosec hardcoded_sql_expressions
        )

    # remove existing data from the results
    existing_data_hashes = list(
        pd.read_sql(
            f"SELECT * FROM '{task_hash}' ",  # nosec hardcoded_sql_expressions
            project_db_con,
        )["datapoint_hash"]
    )
    data_w_hash = data_w_hash[
        ~data_w_hash["datapoint_hash"].isin(existing_data_hashes)
    ].reset_index(drop=True)

    # save results to db
    if show_datapoints_in_results_db:
        data_w_hash.to_sql(
            f"{task_hash}", con=project_db_con, if_exists="append", index=False
        )
    else:
        data_w_hash[["datapoint_hash", _RESULTS_COLUMN_NAME]].to_sql(
            f"{task_hash}", con=project_db_con, if_exists="append", index=False
        )
    # import pdb; pdb.set_trace()
    logger.info("Results saved to database")
