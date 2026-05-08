from app.database.connection import db_connection
from app.utils.logger import get_logger


logger = get_logger(__name__)


class ProcessingLogRepository:
    """
    Stores processing events in the database.

    File logs tell developers what happened.
    Database logs tell the application what happened.
    """

    def create_log(
        self,
        document_id: int | None,
        step_name: str,
        status: str,
        message: str,
    ) -> None:
        query = """
            INSERT INTO processing_logs (
                document_id,
                step_name,
                status,
                message
            )
            VALUES (%s, %s, %s, %s);
        """

        connection = db_connection.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (document_id, step_name, status, message),
                )

            connection.commit()

        except Exception as error:
            connection.rollback()
            logger.error("Failed to create processing log: %s", error)
            raise