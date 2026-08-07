from src.embeddings.embedding_service import EmbeddingService
from src.logging.logger import setup_logger

logger = setup_logger(__name__)


class QueryEmbedder:
    """
    Generates an embedding vector for a user query.

    Keeps query embedding logic separate from the retrieval layer
    so the embedding provider can be changed independently.
    """

    @staticmethod
    def embed(query: str) -> list[float]:
        """
        Generate an embedding for the supplied query.

        Args:
            query: User's search/query text.

        Returns:
            Embedding vector as a list of floats.

        Raises:
            ValueError: If the query is empty.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        query = query.strip()

        logger.debug(
            "Generating query embedding. Query length=%d",
            len(query),
        )

        try:
            embedding = EmbeddingService.embed(query)

            if not embedding:
                raise ValueError(
                    "Embedding service returned an empty embedding."
                )

            logger.debug(
                "Query embedding generated successfully. Dimensions=%d",
                len(embedding),
            )

            return embedding

        except Exception:
            logger.exception(
                "Failed to generate query embedding."
            )
            raise