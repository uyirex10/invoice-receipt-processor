from pathlib import Path

from app.ocr.pdf_text_extractor import PDFTextExtractor
from app.ocr.tesseract_ocr import TesseractOCR
from app.utils.logger import get_logger


logger = get_logger(__name__)


class TextExtractionService:
    """
    Coordinates document text extraction workflow.

    Responsibilities:
    - Detect file type
    - Try PDF text extraction first
    - Fallback to OCR when necessary

    It should NOT:
    - Parse invoice data
    - Validate invoice fields
    - Save database records
    """

    MINIMUM_TEXT_LENGTH = 20

    def __init__(
        self,
        pdf_extractor: PDFTextExtractor,
        ocr_engine: TesseractOCR,
    ):
        self.pdf_extractor = pdf_extractor
        self.ocr_engine = ocr_engine

    def extract_text(self, file_path: str) -> str:
        file_path = Path(file_path)

        logger.info("Starting text extraction workflow.")

        if file_path.suffix.lower() == ".pdf":

            extracted_text = self.pdf_extractor.extract_text(file_path)

            if len(extracted_text.strip()) >= self.MINIMUM_TEXT_LENGTH:
                logger.info(
                    "PDF direct extraction successful. OCR skipped."
                )
                return extracted_text

            logger.warning(
                "PDF text extraction insufficient. Falling back to OCR."
            )

        extracted_text = self.ocr_engine.extract_text(file_path)

        return extracted_text