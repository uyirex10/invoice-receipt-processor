from app.ai.ai_invoice_extractor import AIInvoiceExtractor
from app.ai.ollama_client import OllamaClient
from app.database.repositories.document_repository import (
    DocumentRepository,
)
from app.database.repositories.invoice_repository import (
    InvoiceRepository,
)
from app.database.repositories.processing_log_repository import (
    ProcessingLogRepository,
)
from app.extraction.invoice_extractor import InvoiceExtractor
from app.normalizers.invoice_normalizer import (
    InvoiceNormalizer,
)
from app.ocr.pdf_text_extractor import PDFTextExtractor
from app.ocr.tesseract_ocr import TesseractOCR
from app.ocr.text_extraction_service import (
    TextExtractionService,
)
from app.services.document_service import (
    DocumentService,
    DuplicateDocumentError,
)
from app.services.invoice_processing_service import (
    InvoiceProcessingService,
)
from app.storage.file_storage_service import (
    FileStorageService,
)
from app.utils.logger import get_logger
from app.validators.invoice_validator import (
    InvoiceValidator,
)


logger = get_logger(__name__)


def main() -> None:
    """
    Full end-to-end invoice processing pipeline test.

    Workflow:
    Upload
        ↓
    OCR/Text Extraction
        ↓
    Regex Extraction
        ↓
    AI Fallback (if needed)
        ↓
    Normalization
        ↓
    Validation
        ↓
    Duplicate Detection
        ↓
    Database Save
    """

    # =========================================================
    # Infrastructure / Shared Services
    # =========================================================

    storage_service = FileStorageService()

    document_repository = DocumentRepository()

    invoice_repository = InvoiceRepository()

    processing_log_repository = (
        ProcessingLogRepository()
    )

    # =========================================================
    # Document Upload Workflow
    # =========================================================

    document_service = DocumentService(
        storage_service=storage_service,
        document_repository=document_repository,
        processing_log_repository=processing_log_repository,
    )

    # =========================================================
    # OCR / Text Extraction Layer
    # =========================================================

    text_extraction_service = TextExtractionService(
        pdf_extractor=PDFTextExtractor(),
        ocr_engine=TesseractOCR(),
    )

    # =========================================================
    # AI Extraction Layer
    # =========================================================

    ai_extractor = AIInvoiceExtractor(
        llm_client=OllamaClient(
            model_name="phi"
        )
    )

    # =========================================================
    # Invoice Processing Workflow
    # =========================================================

    invoice_processing_service = (
        InvoiceProcessingService(
            text_extraction_service=text_extraction_service,

            invoice_extractor=InvoiceExtractor(
                ai_invoice_extractor=ai_extractor
            ),

            invoice_normalizer=InvoiceNormalizer(),

            invoice_validator=InvoiceValidator(),

            invoice_repository=invoice_repository,

            processing_log_repository=(
                processing_log_repository
            ),
        )
    )

    # =========================================================
    # Test File
    # =========================================================

    sample_file = (
        "sample_files/samp_invoice.jpg"
    )

    try:

        # =====================================================
        # Step 1: Upload Document
        # =====================================================

        upload_result = (
            document_service.upload_document(
                sample_file
            )
        )

        logger.info("Upload result:")
        logger.info(upload_result)

        # =====================================================
        # Step 2: Process Invoice
        # =====================================================

        processing_result = (
            invoice_processing_service.process_invoice(
                document_id=upload_result[
                    "document_id"
                ],
                file_path=upload_result[
                    "file_path"
                ],
            )
        )

        logger.info("Processing result:")
        logger.info(processing_result)

    except DuplicateDocumentError as error:

        logger.warning(
            "Duplicate upload detected: %s",
            error,
        )

    except Exception as error:

        logger.error(
            "Full pipeline failed: %s",
            error,
        )


if __name__ == "__main__":
    main()