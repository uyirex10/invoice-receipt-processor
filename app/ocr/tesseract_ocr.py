from pathlib import Path

import pytesseract
from PIL import Image

from app.ocr.base_ocr import BaseOCR
from app.ocr.image_preprocessor import ImagePreprocessor
from app.utils.logger import get_logger


logger = get_logger(__name__)


class TesseractOCR(BaseOCR):
    """
    OCR implementation using Tesseract.

    Responsibilities:
    - Preprocess image
    - Run OCR extraction
    - Return extracted text

    It should NOT:
    - Validate text
    - Parse invoices
    - Save database records
    """

    # Change this path if your installation differs.
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    def __init__(self):
        self.preprocessor = ImagePreprocessor()

    def extract_text(
            self,
            file_path: str | Path,
            use_preprocessing: bool = True,
    ) -> str:
        file_path = Path(file_path)

        logger.info("Starting OCR extraction for file=%s", file_path)

        try:
            image_path_to_use = file_path

            # Optional preprocessing step.
            if use_preprocessing:
                logger.info("Using OCR preprocessing pipeline.")

                image_path_to_use = self.preprocessor.preprocess_for_ocr(
                    file_path
                )

            else:
                logger.info("Skipping OCR preprocessing.")

            image = Image.open(image_path_to_use)

            extracted_text = pytesseract.image_to_string(image)

            logger.info("OCR extraction completed successfully.")

            return extracted_text.strip()

        except Exception as error:
            logger.error("OCR extraction failed: %s", error)
            raise