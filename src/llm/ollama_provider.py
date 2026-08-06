from ollama import Client

from src.llm.llm_provider import BaseLLM
from src.llm.llm_config import OLLAMA_MODEL


class OllamaProvider(BaseLLM):

    def __init__(self):

        self.client = Client(
            host="http://localhost:11434"
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.chat(

            model=OLLAMA_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response["message"]["content"]