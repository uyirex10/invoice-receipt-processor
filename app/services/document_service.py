from pathlib import Path

from app.database.repositories.document_repository import DocumentRepository
from app.database.repositories.processing_log_repository import (
    ProcessingLogRepository,
)
from app.storage.file_storage_service import FileStorageService
from app.utils.file_hash import generate_file_hash
from app.utils.logger import get_logger


logger = get_logger(__name__)


class DuplicateDocumentError(Exception):
    """
    Raised when a duplicate document is detected.
    """


class DocumentService:
    """
    Handles document upload workflow.

    Responsibilities:
    - Save uploaded file
    - Generate file hash
    - Detect duplicate uploads
    - Create document database record
    - Create processing logs

    It should NOT:
    - Run OCR
    - Parse invoices
    - Validate invoice data
    """

    def __init__(
        self,
        storage_service: FileStorageService,
        document_repository: DocumentRepository,
        processing_log_repository: ProcessingLogRepository,
    ):
        self.storage_service = storage_service
        self.document_repository = document_repository
        self.processing_log_repository = processing_log_repository

    def upload_document(self, source_file_path: str) -> dict:
        """
        Handles document upload process.
        """

        logger.info("Starting document upload workflow.")

        saved_file_path = self.storage_service.save_file(source_file_path)

        file_hash = generate_file_hash(saved_file_path)

        existing_document = self.document_repository.find_by_file_hash(file_hash)

        if existing_document:
            logger.warning(
                "Duplicate document detected for hash=%s",
                file_hash,
            )

            raise DuplicateDocumentError(
                "This document already exists in the system."
            )

        document_id = self.document_repository.create_document(
            file_name=Path(source_file_path).name,
            file_path=str(saved_file_path),
            file_hash=file_hash,
            file_type=saved_file_path.suffix.lower(),
        )

        self.processing_log_repository.create_log(
            document_id=document_id,
            step_name="DOCUMENT_UPLOAD",
            status="SUCCESS",
            message="Document uploaded successfully.",
        )

        logger.info(
            "Document upload completed successfully. document_id=%s",
            document_id,
        )

        return {
            "document_id": document_id,
            "file_path": str(saved_file_path),
            "file_hash": file_hash,
            "status": "uploaded",
        }