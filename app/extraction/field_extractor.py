import re
from decimal import Decimal
from typing import Optional

from app.utils.logger import get_logger


logger = get_logger(__name__)


class FieldExtractor:
    """
    Extracts individual invoice fields from raw text.

    Responsibilities:
    - Extract invoice number
    - Extract amount
    - Extract date
    - Extract vendor name

    It should NOT:
    - Validate fields
    - Save database records
    - Run OCR
    """

    AMOUNT_PATTERNS = [
        r"TOTAL[:\s]*₦?\s?([\d,]+(?:\.\d{2})?)",
        r"AMOUNT DUE[:\s]*₦?\s?([\d,]+(?:\.\d{2})?)",
        r"GRAND TOTAL[:\s]*₦?\s?([\d,]+(?:\.\d{2})?)",
    ]

    INVOICE_NUMBER_PATTERNS = [
        r"INVOICE\s*#?\s*[:\-]?\s*([A-Z0-9\-]+)",
        r"INV[:\-]?\s*([A-Z0-9\-]+)",
    ]

    DATE_PATTERNS = [
        r"(\d{2}/\d{2}/\d{4})",
        r"(\d{4}-\d{2}-\d{2})",
    ]

    def extract_total_amount(
        self,
        text: str,
    ) -> Optional[Decimal]:
        """
        Extracts invoice total amount.
        """

        for pattern in self.AMOUNT_PATTERNS:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                raw_amount = match.group(1)

                cleaned_amount = raw_amount.replace(",", "")

                try:
                    amount = Decimal(cleaned_amount)

                    logger.info(
                        "Total amount extracted successfully: %s",
                        amount,
                    )

                    return amount

                except Exception:
                    logger.warning(
                        "Failed to parse amount: %s",
                        cleaned_amount,
                    )

        logger.warning("Total amount not found.")

        return None

    def extract_invoice_number(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Extracts invoice number.
        """

        for pattern in self.INVOICE_NUMBER_PATTERNS:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                invoice_number = match.group(1).strip()

                logger.info(
                    "Invoice number extracted successfully: %s",
                    invoice_number,
                )

                return invoice_number

        logger.warning("Invoice number not found.")

        return None

    def extract_invoice_date(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Extracts invoice date.
        """

        for pattern in self.DATE_PATTERNS:

            match = re.search(pattern, text)

            if match:
                invoice_date = match.group(1)

                logger.info(
                    "Invoice date extracted successfully: %s",
                    invoice_date,
                )

                return invoice_date

        logger.warning("Invoice date not found.")

        return None

    def extract_vendor_name(
        self,
        text: str,
    ) -> Optional[str]:
        """
        Extracts vendor name.

        Current strategy:
        Assume first non-empty line is vendor.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            logger.warning("Vendor name not found.")

            return None

        vendor_name = lines[0]

        logger.info(
            "Vendor name extracted successfully: %s",
            vendor_name,
        )

        return vendor_name