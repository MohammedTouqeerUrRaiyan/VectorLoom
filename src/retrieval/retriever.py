from src.logging.logger import setup_logger
from src.retrieval.query_embedder import QueryEmbedder
from src.vector_store.store_service import StoreService

logger = setup_logger(__name__)


class Retriever:
    """
    Dense vector retriever backed by ChromaDB.
    """

    @staticmethod
    def retrieve(
        query: str,
        k: int = 5,
    ):
        """
        Retrieve the most relevant chunks using vector similarity.
        """

        if not query or not query.strip():
            raise ValueError(
                "Retriever query cannot be empty."
            )

        if k <= 0:
            raise ValueError(
                "Retriever k must be greater than zero."
            )

        query = query.strip()

        logger.info(
            "Starting vector retrieval. k=%d",
            k,
        )

        query_embedding = QueryEmbedder.embed(
            query
        )

        results = StoreService.search(
            query_embedding,
            k,
        )

        result_count = 0

        try:
            result_count = len(
                results.get("ids", [[]])[0]
            )
        except (
            AttributeError,
            IndexError,
            TypeError,
        ):
            pass

        logger.info(
            "ChromaDB vector retrieval completed. "
            "Results=%d",
            result_count,
        )

        return results