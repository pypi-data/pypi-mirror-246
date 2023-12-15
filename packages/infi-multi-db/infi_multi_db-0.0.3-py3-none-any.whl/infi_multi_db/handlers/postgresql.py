import psycopg2
import logging
from typing import Dict, Union, List, Tuple, Optional, Any


class PostgresSQL:
    def __init__(self, connection_params: Dict[str, Union[str, int]]):
        """
        Initialize the PostgreSQLHandler instance.

        Parameters:
            - connection_params (dict): Parameters required to establish a connection to the PostgreSQL database.
                Example:
                {
                    "dbname": "your_database_name",
                    "user": "your_username",
                    "password": "your_password",
                    "host": "your_host",
                    "port": "your_port",
                }
        """
        self.connection_params = connection_params
        self.connection = None
        self.cursor = None

    def start_connection(self) -> None:
        """
        Start the connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            logging.info("Connection to PostgreSQL established.")
        except Exception as e:
            logging.error("Error starting connection: %s", e)
            raise e

    def stop_connection(self) -> None:
        """
        Stop the connection to the PostgreSQL database.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                logging.info("Connection to PostgreSQL closed.")
        except Exception as e:
            logging.error("Error stopping connection: %s", e)
            raise e

    def create_table(self, table_name: str, columns: List[Tuple[str, str]]) -> None:
        """
        Create a table in the PostgreSQL database.

        Parameters:
            - table_name (str): Name of the table.
            - columns (list): List of tuples representing column names and their types.
        """
        try:
            query = "CREATE TABLE {} ({});".format(
                table_name,
                ", ".join(
                    "{} {}".format(col_name, col_type) for col_name, col_type in columns
                ),
            )
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Table %s created successfully.", table_name)
        except Exception as e:
            logging.error("Error creating table: %s", e)
            raise e

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the PostgreSQL database.

        Parameters:
            - table_name (str): Name of the table to be deleted.
        """
        try:
            query = "DROP TABLE IF EXISTS {};".format(table_name)
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Table %s deleted successfully.", table_name)
        except Exception as e:
            logging.error("Error deleting table: %s", e)
            raise e

    def update_table(self, table_name: str, new_columns: List[Tuple[str, str]]) -> None:
        """
        Update a table in the PostgreSQL database.

        Parameters:
            - table_name (str): Name of the table to be updated.
            - new_columns (list): List of tuples representing new column names and their types.
        """
        try:
            query = "ALTER TABLE {} ".format(table_name)
            query += ", ".join(
                "ADD COLUMN {} {}".format(col_name, col_type)
                for col_name, col_type in new_columns
            )
            query += ";"
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Table %s updated successfully.", table_name)
        except Exception as e:
            logging.error("Error updating table: %s", e)
            raise e

    def get_all_records_from_table(self, table_name: str) -> List[Dict[str, Union[str, int, float]]]:
        """
        Get all records from the specified table.

        Parameters:
            - table_name (str): Name of the table.

        Returns:
            - List[Dict[str, Union[str, int, float]]]: List of dictionaries representing all records in the table.
        """
        try:
            query = "SELECT * FROM {};".format(table_name)
            self.cursor.execute(query)
            records = [
                dict(zip([column[0] for column in self.cursor.description], row))
                for row in self.cursor.fetchall()
            ]
            logging.info("Retrieved all records from table %s.", table_name)
            return records
        except Exception as e:
            logging.error("Error getting table: %s", e)
            raise e

    def get_tables(self) -> List[str]:
        """
        Get a list of table names in the database.

        Returns:
            - List[str]: List of table names.
        """
        try:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            self.cursor.execute(query)
            table_names = [row[0] for row in self.cursor.fetchall()]
            logging.info("Retrieved table names: %s", table_names)
            return table_names
        except Exception as e:
            logging.error("Error getting tables: %s", e)
            raise e

    def create_record(
            self, table_name: str, record_data: Dict[str, Union[str, int, float]]
    ) -> None:
        """
        Create a record in the specified table.

        Parameters:
            - table_name (str): Name of the table.
            - record_data (dict): Dictionary representing the record data.
        """
        try:
            columns = ", ".join(record_data.keys())
            values = ", ".join("'{}'".format(value) for value in record_data.values())
            query = "INSERT INTO {} ({}) VALUES ({});".format(
                table_name, columns, values
            )
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Record created successfully in table %s.", table_name)
        except Exception as e:
            logging.error("Error creating record: %s", e)
            raise e

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
        try:
            set_values = ", ".join(
                "{}='{}'".format(col_name, col_value)
                for col_name, col_value in new_data.items()
            )
            query = "UPDATE {} SET {} WHERE {}={};".format(
                table_name, set_values, record_id_column, record_id
            )
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Record updated successfully in table %s.", table_name)
        except Exception as e:
            logging.error("Error updating record: %s", e)
            raise e

    def read_records(
            self,
            table_name: str,
            query: Optional[str] = None,
            select_columns: Optional[list] = None
    ) -> List[Dict[str, Union[str, int, float]]]:
        """
        Read records from the specified table based on the given query.

        Parameters:
            - table_name (str): Name of the table.
            - query (str, optional): Query to filter records.
            - select_columns (list, optional): List of columns to select.

        Returns:
            - List[Dict[str, Union[str, int, float]]]: List of dictionaries representing the retrieved records.
        """
        try:
            if select_columns:
                select_clause = ', '.join(f'"{col}"' for col in select_columns)
            else:
                select_clause = '*'

            if query:
                full_query = f"SELECT {select_clause} FROM {table_name} WHERE {query};"
            else:
                full_query = f"SELECT {select_clause} FROM {table_name};"

            self.cursor.execute(full_query)
            records = [
                dict(zip([column[0] for column in self.cursor.description], row))
                for row in self.cursor.fetchall()
            ]
            logging.info("Read %d records from table %s.", len(records), table_name)
            return records
        except Exception as e:
            logging.error("Error reading records: %s", e)
            raise e

    def remove_record(self, table_name: str, record_id: int) -> None:
        """
        Remove a record from the specified table.

        Parameters:
            - table_name (str): Name of the table.
            - record_id (int): ID of the record to be removed.
        """
        try:
            query = "DELETE FROM {} WHERE id={};".format(table_name, record_id)
            self.cursor.execute(query)
            self.connection.commit()
            logging.info(
                "Record with ID %d removed from table %s.", record_id, table_name
            )
        except Exception as e:
            logging.error("Error removing record: %s", e)
            raise e

    def execute_custom_sql(self, sql_command: str) -> Any:
        """
        Execute a custom SQL command on the PostgreSQL database.

        Parameters:
            - sql_command (str): The custom SQL command to execute.

        Returns:
            - Any: The result of the SQL command execution.
        """
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            result = self.cursor.fetchall()
            logging.info("Custom SQL command executed successfully.")
            return result
        except Exception as e:
            logging.error("Error executing custom SQL command: %s", e)
            raise e
