from app.database.repositories.invoice_repository import InvoiceRepository
from app.database.repositories.processing_log_repository import (
    ProcessingLogRepository,
)
from app.extraction.invoice_extractor import InvoiceExtractor
from app.normalizers.invoice_normalizer import InvoiceNormalizer
from app.ocr.text_extraction_service import TextExtractionService
from app.utils.logger import get_logger
from app.validators.invoice_validator import InvoiceValidator


logger = get_logger(__name__)


class InvoiceProcessingService:
    """
    Coordinates full invoice processing workflow.

    Responsibilities:
    - Extract text
    - Extract invoice fields
    - Normalize data
    - Validate data
    - Save invoice
    - Save processing logs

    It should NOT:
    - Handle file uploads
    - Handle API requests
    """

    def __init__(
        self,
        text_extraction_service: TextExtractionService,
        invoice_extractor: InvoiceExtractor,
        invoice_normalizer: InvoiceNormalizer,
        invoice_validator: InvoiceValidator,
        invoice_repository: InvoiceRepository,
        processing_log_repository: ProcessingLogRepository,
    ):
        self.text_extraction_service = text_extraction_service
        self.invoice_extractor = invoice_extractor
        self.invoice_normalizer = invoice_normalizer
        self.invoice_validator = invoice_validator
        self.invoice_repository = invoice_repository
        self.processing_log_repository = processing_log_repository

    def process_invoice(
        self,
        document_id: int,
        file_path: str,
    ) -> dict:
        """
        Full invoice processing workflow.
        """

        logger.info(
            "Starting invoice processing workflow. document_id=%s",
            document_id,
        )

        try:
            # Step 1: Extract raw text.
            raw_text = self.text_extraction_service.extract_text(
                file_path
            )

            # Step 2: Extract invoice fields.
            extracted_data = (
                self.invoice_extractor.extract_invoice_data(
                    raw_text
                )
            )

            # Step 3: Normalize extracted data.
            normalized_data = {
                "document_id": document_id,
                "vendor_name": self.invoice_normalizer.normalize_vendor_name(
                    extracted_data.get("vendor_name")
                ),
                "invoice_number": extracted_data.get(
                    "invoice_number"
                ),
                "invoice_date": self.invoice_normalizer.normalize_date(
                    extracted_data.get("invoice_date")
                ),
                "total_amount": self.invoice_normalizer.normalize_amount(
                    extracted_data.get("total_amount")
                ),
                "confidence_score": extracted_data.get(
                    "confidence_score"
                ),
                "status": "processed",
            }

            # Step 4: Validate normalized data.
            validation_errors = self.invoice_validator.validate(
                normalized_data
            )

            if validation_errors:

                logger.warning(
                    "Invoice validation failed: %s",
                    validation_errors,
                )

                self.processing_log_repository.create_log(
                    document_id=document_id,
                    step_name="VALIDATION",
                    status="FAILED",
                    message=str(validation_errors),
                )

                return {
                    "success": False,
                    "errors": validation_errors,
                    "invoice_data": normalized_data,
                }

            # Step 5: Duplicate invoice detection.
            duplicate_invoice = (
                self.invoice_repository.find_possible_duplicate(
                    vendor_name=normalized_data.get(
                        "vendor_name"
                    ),
                    invoice_number=normalized_data.get(
                        "invoice_number"
                    ),
                    invoice_date=normalized_data.get(
                        "invoice_date"
                    ),
                    total_amount=normalized_data.get(
                        "total_amount"
                    ),
                )
            )

            if duplicate_invoice:

                logger.warning(
                    "Possible duplicate invoice detected."
                )

                self.processing_log_repository.create_log(
                    document_id=document_id,
                    step_name="DUPLICATE_CHECK",
                    status="FAILED",
                    message="Possible duplicate invoice detected.",
                )

                return {
                    "success": False,
                    "errors": [
                        "Possible duplicate invoice detected."
                    ],
                    "invoice_data": normalized_data,
                }

            # Step 6: Save invoice.
            invoice_id = self.invoice_repository.create_invoice(
                normalized_data
            )

            # Step 7: Save success log.
            self.processing_log_repository.create_log(
                document_id=document_id,
                step_name="INVOICE_PROCESSING",
                status="SUCCESS",
                message=f"Invoice processed successfully. invoice_id={invoice_id}",
            )

            logger.info(
                "Invoice processing completed successfully. invoice_id=%s",
                invoice_id,
            )

            return {
                "success": True,
                "invoice_id": invoice_id,
                "invoice_data": normalized_data,
            }

        except Exception as error:

            logger.error(
                "Invoice processing workflow failed: %s",
                error,
            )

            self.processing_log_repository.create_log(
                document_id=document_id,
                step_name="INVOICE_PROCESSING",
                status="FAILED",
                message=str(error),
            )

            raise