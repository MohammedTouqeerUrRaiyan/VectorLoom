from ollama import Client


class StreamingLLM:

    MODEL_NAME = "llama3.2"

    client = Client(host="http://localhost:11434")

    @classmethod
    def generate(cls, prompt: str):

        stream = cls.client.chat(

            model=cls.MODEL_NAME,

            stream=True,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        for chunk in stream:

            yield chunk.message.content