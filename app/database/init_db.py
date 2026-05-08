from pathlib import Path

from app.database.connection import db_connection
from app.utils.logger import get_logger


logger = get_logger(__name__)

SCHEMA_FILE = Path(__file__).parent / "schema.sql"


def initialize_database() -> None:
    """
    Creates all required database tables and indexes.

    Why this exists:
    - Keeps database setup in one controlled place.
    - Makes the project easier to run on another machine.
    - Prevents manual table creation mistakes.
    """

    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")

    connection = db_connection.connect()

    try:
        with connection.cursor() as cursor:
            schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
            cursor.execute(schema_sql)

        connection.commit()
        logger.info("Database schema initialized successfully.")

    except Exception as error:
        connection.rollback()
        logger.error("Database schema initialization failed: %s", error)
        raise

    finally:
        db_connection.close()


if __name__ == "__main__":
    initialize_database()