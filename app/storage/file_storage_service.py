import shutil
from pathlib import Path
from uuid import uuid4

from app.utils.logger import get_logger


logger = get_logger(__name__)


class FileStorageService:
    """
    Handles uploaded file storage.

    Responsibility:
    - Validate file extensions
    - Generate safe unique filenames
    - Save files into uploads directory

    It should NOT:
    - Run OCR
    - Parse invoices
    - Insert database records
    """

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
    }

    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

    def save_file(self, source_path: str) -> Path:
        """
        Saves a file into the uploads directory using a unique filename.
        """

        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(f"File not found: {source}")

        extension = source.suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {extension}")

        unique_filename = f"{uuid4()}{extension}"

        destination = self.upload_dir / unique_filename

        shutil.copy2(source, destination)

        logger.info(
            "File saved successfully: source=%s destination=%s",
            source,
            destination,
        )

        return destination