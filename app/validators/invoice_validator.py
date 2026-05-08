from decimal import Decimal
from typing import Optional

from app.utils.logger import get_logger


logger = get_logger(__name__)


class InvoiceValidator:
    """
    Validates extracted invoice data.

    Responsibilities:
    - Validate required fields
    - Validate amounts
    - Validate dates

    It should NOT:
    - Normalize data
    - Run OCR
    - Save database records
    """

    REQUIRED_FIELDS = [
        "vendor_name",
        "invoice_number",
        "invoice_date",
        "total_amount",
    ]

    def validate(
        self,
        invoice_data: dict,
    ) -> list[str]:
        """
        Returns validation errors.
        """

        errors = []

        errors.extend(
            self.validate_required_fields(invoice_data)
        )

        errors.extend(
            self.validate_total_amount(
                invoice_data.get("total_amount")
            )
        )

        return errors

    def validate_required_fields(
        self,
        invoice_data: dict,
    ) -> list[str]:

        errors = []

        for field in self.REQUIRED_FIELDS:

            if not invoice_data.get(field):
                errors.append(f"Missing required field: {field}")

        return errors

    def validate_total_amount(
        self,
        amount: Optional[Decimal],
    ) -> list[str]:

        errors = []

        if amount is None:
            return errors

        if amount <= Decimal("0"):
            errors.append(
                "Invoice total amount must be greater than zero."
            )

        return errors