import logging

from src.llm.llm_config import LLM_PROVIDER
from src.llm.ollama_provider import OllamaProvider

logger = logging.getLogger(__name__)


class LLMService:

    _provider = None

    @classmethod
    def _get_provider(cls):

        if cls._provider is not None:
            return cls._provider

        if LLM_PROVIDER == "ollama":

            cls._provider = OllamaProvider()

            return cls._provider

        raise ValueError(
            f"Unsupported provider: {LLM_PROVIDER}"
        )

    @classmethod
    def generate(
        cls,
        prompt: str
    ) -> str:

        logger.info(
            "Generating answer..."
        )

        provider = cls._get_provider()

        return provider.generate(prompt)