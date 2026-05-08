from app.ai.ai_invoice_extractor import AIInvoiceExtractor
from app.extraction.field_extractor import FieldExtractor
from app.utils.logger import get_logger


logger = get_logger(__name__)


class InvoiceExtractor:
    """
    Coordinates full invoice extraction workflow.

    Hybrid strategy:
    - Try regex/rule extraction first
    - Use AI fallback when confidence is low
    """

    REQUIRED_FIELDS = [
        "vendor_name",
        "invoice_number",
        "invoice_date",
        "total_amount",
    ]

    AI_FALLBACK_THRESHOLD = 50.0

    def __init__(
        self,
        ai_invoice_extractor: AIInvoiceExtractor | None = None,
    ):
        self.field_extractor = FieldExtractor()

        self.ai_invoice_extractor = ai_invoice_extractor

    def extract_invoice_data(
        self,
        raw_text: str,
    ) -> dict:

        logger.info("Starting invoice extraction workflow.")

        # Step 1: Rule-based extraction.
        extracted_data = {
            "vendor_name": self.field_extractor.extract_vendor_name(raw_text),
            "invoice_number": self.field_extractor.extract_invoice_number(
                raw_text
            ),
            "invoice_date": self.field_extractor.extract_invoice_date(
                raw_text
            ),
            "total_amount": self.field_extractor.extract_total_amount(
                raw_text
            ),
        }

        confidence_score = self.calculate_confidence_score(
            extracted_data
        )

        logger.info(
            "Rule-based extraction confidence=%s",
            confidence_score,
        )

        # Step 2: AI fallback if confidence is low.
        if (
            confidence_score < self.AI_FALLBACK_THRESHOLD
            and self.ai_invoice_extractor
        ):

            logger.warning(
                "Low confidence extraction detected. Triggering AI fallback."
            )

            ai_result = (
                self.ai_invoice_extractor.extract_invoice_data(
                    raw_text
                )
            )

            extracted_data = self.merge_extraction_results(
                regex_result=extracted_data,
                ai_result=ai_result,
            )

            confidence_score = self.calculate_confidence_score(
                extracted_data
            )

            logger.info(
                "Post-AI extraction confidence=%s",
                confidence_score,
            )

        extracted_data["confidence_score"] = confidence_score

        logger.info(
            "Invoice extraction workflow completed successfully."
        )

        return extracted_data

    def merge_extraction_results(
        self,
        regex_result: dict,
        ai_result: dict,
    ) -> dict:
        """
        Merges regex and AI extraction results.

        Strategy:
        - Prefer regex when available
        - Use AI only for missing fields
        """

        merged = regex_result.copy()

        for key, value in ai_result.items():

            if not merged.get(key) and value:
                merged[key] = value

        return merged

    def calculate_confidence_score(
        self,
        extracted_data: dict,
    ) -> float:

        successful_fields = 0

        for field in self.REQUIRED_FIELDS:

            if extracted_data.get(field):
                successful_fields += 1

        confidence_score = (
            successful_fields / len(self.REQUIRED_FIELDS)
        ) * 100

        return round(confidence_score, 2)