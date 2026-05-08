import psycopg2
from psycopg2.extensions import connection

from app.config.settings import settings
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DatabaseConnection:
    """
    Handles PostgreSQL database connections.

    Why this class exists:
    - Keeps database connection logic in one place.
    - Makes it easier to change connection strategy later.
    - Prevents random database connections across the app.
    """

    def __init__(self):
        self._connection: connection | None = None

    def connect(self) -> connection:
        """
        Opens a database connection if one does not already exist.
        """

        if self._connection and not self._connection.closed:
            return self._connection

        try:
            self._connection = psycopg2.connect(
                dbname=settings.db_name,
                user=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
            )

            logger.info("Database connection established successfully.")
            return self._connection

        except psycopg2.Error as error:
            logger.error("Database connection failed: %s", error)
            raise

    def close(self) -> None:
        """
        Closes the active database connection.
        """

        if self._connection and not self._connection.closed:
            self._connection.close()
            logger.info("Database connection closed.")


db_connection = DatabaseConnection()