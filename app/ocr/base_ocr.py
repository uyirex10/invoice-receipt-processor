from abc import ABC, abstractmethod
from pathlib import Path


class BaseOCR(ABC):
    """
    Base interface for OCR engines.

    Why this exists:
    - Makes OCR engines interchangeable.
    - Allows future replacement of Tesseract with cloud OCR.
    """

    @abstractmethod
    def extract_text(self, file_path: str | Path) -> str:
        """
        Extracts text from document/image.
        """