from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Base interface for AI models.

    Why this exists:
    - Makes AI providers interchangeable.
    - Allows future switch to OpenAI, Claude, Gemini, etc.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generates model response.
        """