from app.database.connection import db_connection
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    """
    Application entry point.

    For now, this only tests whether our foundation works:
    - logging
    - environment loading
    - database connection
    """

    logger.info("Application started.")

    connection = db_connection.connect()

    if connection:
        logger.info("Database test successful.")

    db_connection.close()

    logger.info("Application finished.")


if __name__ == "__main__":
    main()