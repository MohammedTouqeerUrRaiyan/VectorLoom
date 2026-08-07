from rank_bm25 import BM25Okapi

from src.logging.logger import setup_logger


logger = setup_logger(__name__)


class BM25Retriever:
    """
    Lightweight BM25 lexical retriever.

    Builds a BM25 index from RetrievedChunk objects and
    returns the most relevant chunks for a query.
    """

    def __init__(self):
        self.documents = []
        self.metadata = []
        self.bm25 = None

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """
        Basic tokenizer used by both documents and queries.
        """

        if not text:
            return []

        return text.lower().split()

    def build_index(self, chunks):
        """
        Build the BM25 index from retrieved chunks.
        """

        if not chunks:
            logger.warning(
                "Empty chunk list provided to BM25 index builder."
            )

            self.documents = []
            self.metadata = []
            self.bm25 = None

            return

        self.documents = [
            chunk.text
            for chunk in chunks
        ]

        self.metadata = list(chunks)

        tokenized_documents = [
            self._tokenize(document)
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

        logger.info(
            "BM25 index built successfully. Documents=%d",
            len(self.documents),
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Search the BM25 index.

        Important:
        We do NOT discard zero-score results.

        With very small document collections,
        BM25 can legitimately produce zero IDF
        for terms appearing in every document.
        """

        logger.info(
            "BM25 search started. Query='%s' top_k=%d",
            query,
            top_k,
        )

        if self.bm25 is None:
            logger.warning(
                "BM25 index is not initialized."
            )
            return []

        if not query or not query.strip():
            logger.warning(
                "BM25 query is empty."
            )
            return []

        query_tokens = self._tokenize(query)

        if not query_tokens:
            logger.warning(
                "BM25 query produced no tokens."
            )
            return []

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked = sorted(
            zip(scores, self.metadata),
            key=lambda item: item[0],
            reverse=True,
        )

        # Do NOT use:
        #
        # if score > 0
        #
        # Zero is a valid BM25 score.

        results = [
            chunk
            for _, chunk in ranked[:top_k]
        ]

        logger.info(
            "BM25 search completed. Results=%d",
            len(results),
        )

        return results