"""Class AuroraDatabase."""
import warnings
from os import getenv

from pandas import DataFrame
from pandas import read_sql

from mysql.connector import CMySQLConnection
from mysql.connector import Error
from mysql.connector import MySQLConnection
from mysql.connector import connect
from mysql.connector.pooling import PooledMySQLConnection


warnings.simplefilter(action="ignore", category=UserWarning)


class AuroraDatabase:
    """Class for managing aurora database connection.

    This class provides methods to establish and manage a database connection
    and execute SQL queries.
    """

    def __init__(self, is_connection_string: bool = False) -> None:
        """Aurora cosntructor.

        Parameters
        ----------
        is_connection_string : bool, optional
            if connection is from string, by default False
        """
        self.__is_connection_string = is_connection_string
        print("Getting connection to database...")
        self.__connection = self.create_connection()

    def create_connection(
        self,
    ) -> PooledMySQLConnection | MySQLConnection | CMySQLConnection:
        """Create connection.

        Function that creates the connection to the database.

        Returns
        -------
        PooledMySQLConnection | MySQLConnection | CMySQLConnection
            connector to database.

        Raises
        ------
        Error
            while the connection cannot be stablished.
        """
        if self.__is_connection_string:
            connection_string = getenv("DATABASE_URL", "")
            (
                host,
                database,
                user,
                password,
                port,
            ) = self.__get_db_connection_params_from_string(connection_string)
        else:
            host = getenv("DATABASE_URL_READER", "")
            user = getenv("DATABASE_USER", "")
            password = getenv("DATABASE_PASSWORD", "")
            port = getenv("DATABASE_PORT", "")

        try:
            connection = connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port,
            )
            return connection
        except Error as error:
            raise Exception(
                "An error occurred when trying to connect to the database"
            ) from error

    def execute_query(
        self, query: str, params: dict | None = None
    ) -> DataFrame:
        """Execute query.

        Function that executes the query.

        Parameters
        ----------
        query : str
            The SQL query to execute.

        Returns
        -------
        Dataframe
            Dataframe with the result of query execution.

        Raises
        ------
        Error
            while the query cannot be executed.
        """
        try:
            print("Running query...")
            data = read_sql(query, self.__connection, params=params)
            print("Query executed successfully.")
            return data
        except Error as error:
            raise Exception(
                "An error occurred when trying to execute query!"
            ) from error

    def __get_db_connection_params_from_string(
        self, connection_string: str
    ) -> tuple[str, str, str, str, str]:
        if not connection_string:
            raise ValueError("connection string cannot be None.")

        connection_identity = connection_string.split("/")

        database = connection_identity[3]

        connection_identity = connection_identity[2].split(":")

        user = connection_identity[0]
        port = connection_identity[2]

        connection_identity = connection_identity[1].split("@")

        password = connection_identity[0]
        host = connection_identity[1]

        return host, database, user, password, port

    @property
    def connection(
        self,
    ) -> PooledMySQLConnection | MySQLConnection | CMySQLConnection:
        """Connection getter.

        Returns
        -------
        PooledMySQLConnection | MySQLConnection | CMySQLConnection
            a database connection.
        """
        return self.__connection