from typing import List, Dict, Any, Union, Tuple, Optional

from .handlers.postgresql import PostgresSQL


class MultiDB:
    def __init__(self, db_type: str, connection_params: Dict[str, Any]):
        """
        Initialize the InfiMultyDB instance.

        Parameters:
            - db_type (str): Type of the database (e.g., "postgresql").
            - connection_params (dict): Parameters required to establish a connection to the database.
                Example:
                {
                    "dbname": "your_database_name",
                    "user": "your_username",
                    "password": "your_password",
                    "host": "your_host",
                    "port": "your_port",
                }
        """
        self.db_type = db_type
        self.connection_params = connection_params
        self.db_handler = None

        if self.db_type == "postgresql":
            self.db_handler = PostgresSQL(connection_params)
        # Add conditions for other database types as needed
        else:
            raise ValueError("Unsupported database type: {}".format(self.db_type))

    def start_connection(self) -> None:
        """
        Start the connection to the database.
        """
        self.db_handler.start_connection()

    def stop_connection(self) -> None:
        """
        Stop the connection to the database.
        """
        self.db_handler.stop_connection()

    def create_table(self, table_name: str, columns: List[Tuple[str, str]]) -> None:
        """
        Create a table in the database.

        Parameters:
            - table_name (str): Name of the table.
            - columns (list): List of tuples representing column names and their types.
        """
        self.db_handler.create_table(table_name, columns)

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the database.

        Parameters:
            - table_name (str): Name of the table to be deleted.
        """
        self.db_handler.delete_table(table_name)

    def update_table(self, table_name: str, new_columns: List[Tuple[str, str]]) -> None:
        """
        Update a table in the database.

        Parameters:
            - table_name (str): Name of the table to be updated.
            - new_columns (list): List of tuples representing new column names and their types.
        """
        self.db_handler.update_table(table_name, new_columns)

    def get_all_records_from_table(self, table_name: str) -> List[Dict[str, Union[str, int, float]]]:
        """
        Get all records from the specified table.

        Parameters:
            - table_name (str): Name of the table.

        Returns:
            - List[Dict[str, Union[str, int, float]]]: List of dictionaries representing all records in the table.
        """
        return self.db_handler.get_all_records_from_table(table_name)

    def get_tables(self) -> List[str]:
        """
        Get a list of table names in the database.

        Returns:
            - List[str]: List of table names.
        """
        return self.db_handler.get_tables()

    def create_record(
        self, table_name: str, record_data: Dict[str, Union[str, int, float]]
    ) -> None:
        """
        Create a record in the specified table.

        Parameters:
            - table_name (str): Name of the table.
            - record_data (dict): Dictionary representing the record data.
        """
        self.db_handler.create_record(table_name, record_data)

    def update_record(
        self,
        table_name: str,
        record_id: int,
        new_data: Dict[str, Union[str, int, float]],
        record_id_column: str = "id"
    ) -> None:
        """
        Update a record in the specified table.

        Parameters:
            - table_name (str): Name of the table.
            - record_id (int): ID of the record to be updated.
            - new_data (dict): Dictionary representing the new data for the record.
            - record_id_column (str): Name of the column containing the record identifier.
        """
        self.db_handler.update_record(table_name, record_id, new_data, record_id_column)

    def read_records(
            self, table_name: str, query: str, select_columns: Optional[list] = None
    ) -> List[Dict[str, Union[str, int, float]]]:
        """
        Read records from the specified table based on the given query.

        Parameters:
            - table_name (str): Name of the table.
            - query (str): Query to filter records.
            - select_columns (list, optional): List of columns to select.

        Returns:
            - List[Dict[str, Union[str, int, float]]]: List of dictionaries representing the retrieved records.
        """
        if select_columns:
            records = self.db_handler.read_records(table_name, query, select_columns)
        else:
            records = self.db_handler.read_records(table_name, query)

        return records if records is not None else []

    def remove_record(self, table_name: str, record_id: int) -> None:
        """
        Remove a record from the specified table.

        Parameters:
            - table_name (str): Name of the table.
            - record_id (int): ID of the record to be removed.
        """
        self.db_handler.remove_record(table_name, record_id)

    def execute_custom_sql(self, sql_command: str) -> Any:
        """
        Execute a custom SQL command on the database.

        Parameters:
            - sql_command (str): The custom SQL command to execute.

        Returns:
            - Any: The result of the SQL command execution.
        """
        return self.db_handler.execute_custom_sql(sql_command)
