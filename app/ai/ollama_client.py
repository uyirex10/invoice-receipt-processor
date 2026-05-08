import time

import requests

from app.ai.base_llm import BaseLLM
from app.utils.logger import get_logger


logger = get_logger(__name__)


class OllamaClient(BaseLLM):
    """
    Ollama local LLM client with retry handling.
    """

    def __init__(
        self,
        model_name: str = "phi",
        base_url: str = "http://localhost:11434/api/generate",
        timeout: int = 180,
        max_retries: int = 3,
    ):
        self.model_name = model_name
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def generate(self, prompt: str) -> str:

        logger.info(
            "Sending prompt to Ollama model=%s",
            self.model_name,
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }

        last_error = None

        for attempt in range(1, self.max_retries + 1):

            try:

                logger.info(
                    "Ollama request attempt=%s",
                    attempt,
                )

                response = requests.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                result = response.json()

                generated_text = result.get(
                    "response",
                    "",
                )

                logger.info(
                    "Ollama response received successfully."
                )

                return generated_text.strip()

            except Exception as error:

                last_error = error

                logger.warning(
                    "Ollama request failed on attempt=%s error=%s",
                    attempt,
                    error,
                )

                # Small delay before retry.
                time.sleep(2)

        logger.error(
            "Ollama generation failed after retries: %s",
            last_error,
        )

        raise last_error