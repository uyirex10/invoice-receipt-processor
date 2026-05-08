from decimal import Decimal
from typing import Any

from app.database.connection import db_connection
from app.utils.logger import get_logger


logger = get_logger(__name__)


class InvoiceRepository:
    """
    Handles database operations for invoices and line items.

    Responsibility:
    - Create invoice records
    - Batch insert line items
    - Find possible duplicate invoices

    It should NOT:
    - Run OCR
    - Validate business rules
    - Categorize expenses
    """

    def create_invoice(self, invoice_data: dict[str, Any]) -> int:
        query = """
            INSERT INTO invoices (
                document_id,
                vendor_name,
                invoice_number,
                invoice_date,
                total_amount,
                tax_amount,
                currency,
                category,
                confidence_score,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        connection = db_connection.connect()

        values = (
            invoice_data.get("document_id"),
            invoice_data.get("vendor_name"),
            invoice_data.get("invoice_number"),
            invoice_data.get("invoice_date"),
            invoice_data.get("total_amount"),
            invoice_data.get("tax_amount"),
            invoice_data.get("currency"),
            invoice_data.get("category"),
            invoice_data.get("confidence_score"),
            invoice_data.get("status", "pending"),
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                invoice_id = cursor.fetchone()[0]

            connection.commit()
            logger.info("Invoice created with id=%s", invoice_id)
            return invoice_id

        except Exception as error:
            connection.rollback()
            logger.error("Failed to create invoice: %s", error)
            raise

    def create_line_items(self, invoice_id: int, line_items: list[dict[str, Any]]) -> None:
        """
        Batch inserts line items.

        Performance note:
        This avoids one database commit per line item.
        """

        if not line_items:
            return

        query = """
            INSERT INTO invoice_line_items (
                invoice_id,
                description,
                quantity,
                unit_price,
                total_price
            )
            VALUES (%s, %s, %s, %s, %s);
        """

        values = [
            (
                invoice_id,
                item.get("description"),
                item.get("quantity"),
                item.get("unit_price"),
                item.get("total_price"),
            )
            for item in line_items
        ]

        connection = db_connection.connect()

        try:
            with connection.cursor() as cursor:
                cursor.executemany(query, values)

            connection.commit()
            logger.info(
                "%s line items created for invoice id=%s",
                len(line_items),
                invoice_id,
            )

        except Exception as error:
            connection.rollback()
            logger.error("Failed to create line items: %s", error)
            raise

    def find_possible_duplicate(
        self,
        vendor_name: str | None,
        invoice_number: str | None,
        invoice_date,
        total_amount: Decimal | None,
    ):
        query = """
            SELECT id, vendor_name, invoice_number, invoice_date, total_amount
            FROM invoices
            WHERE
                (
                    invoice_number IS NOT NULL
                    AND invoice_number = %s
                )
                OR
                (
                    vendor_name = %s
                    AND invoice_date = %s
                    AND total_amount = %s
                )
            LIMIT 1;
        """

        connection = db_connection.connect()

        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (invoice_number, vendor_name, invoice_date, total_amount),
            )
            return cursor.fetchone()