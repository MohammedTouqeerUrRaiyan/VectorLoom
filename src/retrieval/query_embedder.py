from src.embeddings.embedding_service import EmbeddingService


class QueryEmbedder:
    """
    Generates embeddings for user queries.
    """

    @staticmethod
    def embed(query: str) -> list[float]:
        return EmbeddingService.embed(query)