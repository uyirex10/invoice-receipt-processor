import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Stores application configuration loaded from environment variables.

    Why this exists:
    - Keeps secrets and environment-specific values out of the code.
    - Makes the app easier to deploy later.
    - Prevents hardcoding database passwords inside files.
    """

    app_name: str = os.getenv("APP_NAME", "Invoice Receipt Processor")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    db_name: str = os.getenv("DB_NAME", "")
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))


settings = Settings()