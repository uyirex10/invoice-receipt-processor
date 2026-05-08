from pathlib import Path

import pdfplumber

from app.utils.logger import get_logger


logger = get_logger(__name__)


class PDFTextExtractor:
    """
    Extracts selectable text directly from PDFs.

    Why this exists:
    - Faster than OCR
    - More accurate than OCR
    - Lower CPU usage

    OCR should only happen if direct extraction fails.
    """

    def extract_text(self, file_path: str | Path) -> str:
        file_path = Path(file_path)

        logger.info("Starting PDF text extraction for file=%s", file_path)

        extracted_text = []

        try:
            with pdfplumber.open(file_path) as pdf:

                for page in pdf.pages:
                    text = page.extract_text()

                    if text:
                        extracted_text.append(text)

            combined_text = "\n".join(extracted_text)

            logger.info("PDF text extraction completed successfully.")

            return combined_text.strip()

        except Exception as error:
            logger.error("PDF text extraction failed: %s", error)
            raise