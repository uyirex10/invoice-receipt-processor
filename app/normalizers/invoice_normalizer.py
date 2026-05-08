from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.utils.logger import get_logger


logger = get_logger(__name__)


class InvoiceNormalizer:
    """
    Normalizes extracted invoice fields.

    Responsibilities:
    - Normalize dates
    - Normalize amounts
    - Normalize vendor names

    It should NOT:
    - Validate business rules
    - Run OCR
    - Save database records
    """

    DATE_FORMATS = [
        "%d/%m/%Y",
        "%Y-%m-%d",
    ]

    def normalize_date(
        self,
        raw_date: Optional[str],
    ) -> Optional[str]:

        if not raw_date:
            return None

        for format_pattern in self.DATE_FORMATS:

            try:
                parsed_date = datetime.strptime(
                    raw_date,
                    format_pattern,
                )

                normalized = parsed_date.strftime("%Y-%m-%d")

                logger.info(
                    "Invoice date normalized successfully: %s",
                    normalized,
                )

                return normalized

            except ValueError:
                continue

        logger.warning("Failed to normalize date: %s", raw_date)

        return None

    def normalize_amount(
        self,
        amount: Optional[Decimal],
    ) -> Optional[Decimal]:

        if amount is None:
            return None

        normalized_amount = amount.quantize(Decimal("0.01"))

        logger.info(
            "Invoice amount normalized successfully: %s",
            normalized_amount,
        )

        return normalized_amount

    def normalize_vendor_name(
        self,
        vendor_name: Optional[str],
    ) -> Optional[str]:

        if not vendor_name:
            return None

        normalized = vendor_name.strip().upper()

        logger.info(
            "Vendor name normalized successfully: %s",
            normalized,
        )

        return normalized