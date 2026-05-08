from pathlib import Path

import cv2

from app.utils.logger import get_logger


logger = get_logger(__name__)


class ImagePreprocessor:
    """
    Prepares images for OCR.

    Responsibilities:
    - Improve image readability
    - Reduce OCR noise
    - Increase text contrast

    It should NOT:
    - Run OCR
    - Parse invoices
    - Save database records
    """

    def preprocess_for_ocr(self, file_path: str | Path) -> str:
        """
        Applies preprocessing techniques and saves processed image.
        """

        file_path = Path(file_path)

        logger.info("Starting image preprocessing for OCR.")

        image = cv2.imread(str(file_path))

        if image is None:
            raise ValueError(f"Could not read image: {file_path}")

        # Convert image to grayscale.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Reduce noise.
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply thresholding for stronger text contrast.
        processed = cv2.threshold(
            blurred,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

        processed_path = file_path.with_name(
            f"{file_path.stem}_processed{file_path.suffix}"
        )

        cv2.imwrite(str(processed_path), processed)

        logger.info(
            "Image preprocessing completed successfully. processed_file=%s",
            processed_path,
        )

        return str(processed_path)