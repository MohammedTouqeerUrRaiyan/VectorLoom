from src.retrieval.query_embedder import QueryEmbedder
from src.vector_store.store_service import StoreService


class Retriever:
    """
    Retrieves the most relevant chunks from ChromaDB.
    """

    @staticmethod
    def retrieve(query: str, k: int = 5):

        query_embedding = QueryEmbedder.embed(query)

        results = StoreService.search(
            query_embedding,
            k
        )

        return results