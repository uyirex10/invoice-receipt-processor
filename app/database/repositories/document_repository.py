from app.database.connection import db_connection
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DocumentRepository:
    """
    Handles database operations for uploaded documents.

    Responsibility:
    - Create document records
    - Find documents by hash
    - Update raw text
    - Update processing status

    It should NOT:
    - Run OCR
    - Parse invoices
    - Validate invoices
    """

    def find_by_file_hash(self, file_hash: str):
        query = """
            SELECT id, file_name, file_path, file_hash, file_type, status
            FROM documents
            WHERE file_hash = %s;
        """

        connection = db_connection.connect()

        with connection.cursor() as cursor:
            cursor.execute(query, (file_hash,))
            return cursor.fetchone()

    def create_document(
        self,
        file_name: str,
        file_path: str,
        file_hash: str,
        file_type: str,
    ) -> int:
        query = """
            INSERT INTO documents (file_name, file_path, file_hash, file_type, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """

        connection = db_connection.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (file_name, file_path, file_hash, file_type, "uploaded"),
                )
                document_id = cursor.fetchone()[0]

            connection.commit()
            logger.info("Document created with id=%s", document_id)
            return document_id

        except Exception as error:
            connection.rollback()
            logger.error("Failed to create document: %s", error)
            raise

    def update_status(self, document_id: int, status: str) -> None:
        query = """
            UPDATE documents
            SET status = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s;
        """

        connection = db_connection.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (status, document_id))

            connection.commit()
            logger.info("Document id=%s status updated to %s", document_id, status)

        except Exception as error:
            connection.rollback()
            logger.error("Failed to update document status: %s", error)
            raise

    def update_raw_text(self, document_id: int, raw_text: str) -> None:
        query = """
            UPDATE documents
            SET raw_text = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s;
        """

        connection = db_connection.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (raw_text, document_id))

            connection.commit()
            logger.info("Raw text updated for document id=%s", document_id)

        except Exception as error:
            connection.rollback()
            logger.error("Failed to update raw text: %s", error)
            raise