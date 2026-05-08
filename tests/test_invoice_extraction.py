from app.extraction.invoice_extractor import InvoiceExtractor
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    """
    Tests invoice extraction workflow.
    """

    extractor = InvoiceExtractor()

    sample_text = """
    SHOPRITE

    Invoice #INV-2026

    Date: 05/05/2026

    TOTAL: ₦15,500
    """

    result = extractor.extract_invoice_data(sample_text)

    logger.info("Extracted invoice data:")
    logger.info(result)


if __name__ == "__main__":
    main()