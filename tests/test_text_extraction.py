from app.ocr.tesseract_ocr import TesseractOCR
from app.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    """
    Compare OCR with and without preprocessing.
    """

    ocr_engine = TesseractOCR()

    sample_file = "sample_files/sample_invoice.jpg"

    logger.info("========== OCR WITHOUT PREPROCESSING ==========")

    raw_result = ocr_engine.extract_text(
        sample_file,
        use_preprocessing=False,
    )

    logger.info("\n%s", raw_result)

    logger.info("========== OCR WITH PREPROCESSING ==========")

    processed_result = ocr_engine.extract_text(
        sample_file,
        use_preprocessing=True,
    )

    logger.info("\n%s", processed_result)


if __name__ == "__main__":
    main()