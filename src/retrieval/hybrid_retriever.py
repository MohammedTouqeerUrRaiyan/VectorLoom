from src.retrieval.query_embedder import QueryEmbedder
from src.retrieval.bm25 import BM25Retriever
from src.vector_store.store_service import StoreService
from src.logging.logger import setup_logger


logger = setup_logger(__name__)


class HybridRetriever:
    """
    Combines semantic vector search with BM25 lexical search.
    """

    def __init__(self):
        self.bm25 = BM25Retriever()

    def build_index(self, chunks):
        """
        Build BM25 index from the available document chunks.
        """

        self.bm25.build_index(chunks)

    def search(
        self,
        question: str,
        chunks,
        top_k: int = 5,
    ):
        """
        Execute vector and BM25 retrieval independently.

        Vector search:
            Uses embeddings and ChromaDB.

        BM25 search:
            Uses lexical keyword matching.

        Both result sets are returned for subsequent
        merging and reranking.
        """

        logger.info(
            "Starting hybrid retrieval. top_k=%d",
            top_k,
        )

        if not question or not question.strip():
            logger.warning(
                "Empty question supplied to hybrid retriever."
            )
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }, []

        if not chunks:
            logger.warning(
                "No chunks supplied to hybrid retriever."
            )
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }, []

        # --------------------------------------------------
        # 1. Build BM25 index
        # --------------------------------------------------

        self.build_index(chunks)

        # --------------------------------------------------
        # 2. Vector Search
        # --------------------------------------------------

        logger.info(
            "Running vector search."
        )

        query_embedding = QueryEmbedder.embed(
            question
        )

        vector_results = StoreService.search(
            query_embedding,
            k=top_k,
        )

        vector_count = len(
            vector_results.get("ids", [[]])[0]
        )

        # --------------------------------------------------
        # 3. BM25 Search
        # --------------------------------------------------

        logger.info(
            "Running BM25 search."
        )

        bm25_results = self.bm25.search(
            question,
            top_k=top_k,
        )

        logger.info(
            "Hybrid retrieval complete. "
            "Vector results=%d, BM25 results=%d",
            vector_count,
            len(bm25_results),
        )

        return vector_results, bm25_results