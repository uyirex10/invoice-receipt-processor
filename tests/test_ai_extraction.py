from app.ai.ai_invoice_extractor import AIInvoiceExtractor
from app.ai.ollama_client import OllamaClient
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:

    llm_client = OllamaClient(model_name="phi")

    extractor = AIInvoiceExtractor(llm_client)

    sample_text = """
    SHOPRITE

    Invoice #INV-2026

    Date: 05/05/2026

    TOTAL: ₦15,500
    """

    result = extractor.extract_invoice_data(sample_text)

    logger.info("AI extraction result:")
    logger.info(result)


if __name__ == "__main__":
    main()