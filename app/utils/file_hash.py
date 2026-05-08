import hashlib
from pathlib import Path


def generate_file_hash(file_path: str | Path) -> str:
    """
    Generates SHA-256 hash for a file.

    Why this exists:
    - Detect duplicate files.
    - Verify file integrity.
    - Avoid processing the same file repeatedly.

    Why SHA-256?
    - Extremely low collision probability.
    - Industry-standard hashing algorithm.
    """

    sha256 = hashlib.sha256()

    file_path = Path(file_path)

    with file_path.open("rb") as file:
        # Read file in chunks instead of loading entire file into memory.
        # Important for large PDFs.
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()