from app.database.repositories.document_repository import DocumentRepository
from app.database.repositories.processing_log_repository import (
    ProcessingLogRepository,
)
from app.services.document_service import (
    DocumentService,
    DuplicateDocumentError,
)
from app.storage.file_storage_service import FileStorageService
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    """
    Tests the complete document upload workflow.
    """

    storage_service = FileStorageService()

    document_repository = DocumentRepository()

    processing_log_repository = ProcessingLogRepository()

    document_service = DocumentService(
        storage_service=storage_service,
        document_repository=document_repository,
        processing_log_repository=processing_log_repository,
    )

    sample_file = "sample_files/sample_invoice.jpg"

    try:
        result = document_service.upload_document(sample_file)

        logger.info("Upload workflow result:")
        logger.info(result)

    except DuplicateDocumentError as error:
        logger.warning("Duplicate detected: %s", error)

    except Exception as error:
        logger.error("Unexpected error: %s", error)


if __name__ == "__main__":
    main()