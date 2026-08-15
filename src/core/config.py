from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # ==========================================================
    # APPLICATION
    # ==========================================================

    APP_NAME: str = "VectorLoom API"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    HOST: str = "127.0.0.1"

    PORT: int = 8000


    # ==========================================================
    # FILE UPLOADS
    # ==========================================================

    UPLOAD_DIR: str = "uploads"

    UPLOAD_FOLDER: str = "data/uploads"

    MAX_FILE_SIZE: int = 10 * 1024 * 1024


    # ==========================================================
    # CHROMADB
    # ==========================================================

    CHROMA_PATH: str = "data/chroma_db"

    COLLECTION_NAME: str = "vectorloom"


    # ==========================================================
    # EMBEDDING
    # ==========================================================

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    EMBEDDING_DIMENSION: int = 384


    # ==========================================================
    # RERANKER
    # ==========================================================

    RERANK_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    RERANK_TOP_K: int = 5


    # ==========================================================
    # RETRIEVAL
    # ==========================================================

    VECTOR_TOP_K: int = 10

    BM25_TOP_K: int = 10

    FINAL_TOP_K: int = 5


    # ==========================================================
    # OLLAMA
    # ==========================================================

    OLLAMA_HOST: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "llama3.2"

    LLM_TEMPERATURE: float = 0.0


    # ==========================================================
    # MEMORY
    # ==========================================================

    MAX_HISTORY: int = 10


    # ==========================================================
    # CACHE
    # ==========================================================

    CACHE_TTL: int = 300


    # ==========================================================
    # LOGGING
    # ==========================================================

    LOG_LEVEL: str = "INFO"


    # ==========================================================
    # ENVIRONMENT
    # ==========================================================

    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"

    )


settings = Settings()