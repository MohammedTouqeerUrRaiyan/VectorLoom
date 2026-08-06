import os

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)

OLLAMA_MODEL = "llama3.2"

OPENAI_MODEL = "gpt-4.1-mini"

GEMINI_MODEL = "gemini-2.5-flash"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")