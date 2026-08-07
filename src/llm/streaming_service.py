from src.llm.ollama_provider import OllamaProvider


class StreamingService:

    @staticmethod
    def stream(prompt: str):

        provider = OllamaProvider()

        return provider.stream(prompt)