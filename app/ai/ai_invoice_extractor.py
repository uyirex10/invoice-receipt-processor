import json
import re

from app.ai.base_llm import BaseLLM
from app.utils.logger import get_logger


logger = get_logger(__name__)


class AIInvoiceExtractor:
    """
    AI-assisted invoice extraction.
    """

    def __init__(self, llm_client: BaseLLM):
        self.llm_client = llm_client

    def extract_invoice_data(
        self,
        raw_text: str,
    ) -> dict:

        prompt = f"""
        You are an invoice extraction system.

        Extract invoice fields from the provided text.

        STRICT RULES:
        - Return ONLY raw JSON
        - Do NOT explain anything
        - Do NOT return markdown
        - Do NOT return Python code
        - Do NOT add comments
        - Do NOT wrap response in triple backticks

        JSON FORMAT:
        {{
            "vendor_name": "string",
            "invoice_number": "string",
            "invoice_date": "string",
            "total_amount": "string"
        }}

        Invoice Text:
        {raw_text}
        """

        logger.info("Starting AI invoice extraction.")

        response = self.llm_client.generate(prompt)

        logger.info("Raw AI response received: %s", response)

        try:
            cleaned_json = self.extract_json(response)

            parsed = json.loads(cleaned_json)

            logger.info(
                "AI invoice extraction completed successfully."
            )

            return parsed

        except Exception as error:

            logger.warning(
                "AI extraction parsing failed: %s",
                error,
            )

            return {}

    def extract_json(
        self,
        response: str,
    ) -> str:
        """
        Extracts JSON object from AI response.
        """

        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL,
        )

        if not match:
            raise ValueError(
                "No JSON object found in AI response."
            )

        return match.group(0)