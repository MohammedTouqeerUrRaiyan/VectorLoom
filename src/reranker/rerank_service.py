from src.logging.logger import setup_logger
from src.reranker.cross_encoder import CrossEncoderModel

logger = setup_logger(__name__)


class RerankService:
    """
    Re-ranks retrieved chunks using a Cross Encoder and filters
    out chunks that are not sufficiently relevant to the question.

    Input:
        - dictionaries
        - Pydantic models
        - compatible objects

    Output:
        - normalized dictionaries containing rerank_score
        - only sufficiently relevant chunks
    """

    # Cross-encoder relevance threshold.
    #
    # Based on the current model behavior:
    #   Relevant VectorLoom chunk  -> approximately +10
    #   Irrelevant chunks          -> approximately -11
    #
    # 0.0 provides a conservative separation boundary.
    RELEVANCE_THRESHOLD = 0.0

    @staticmethod
    def rerank(
        question: str,
        chunks: list,
        top_k: int = 5,
    ) -> list[dict]:

        if not question or not question.strip():
            raise ValueError(
                "Reranker question cannot be empty."
            )

        if not chunks:
            logger.warning(
                "Reranker received no chunks."
            )
            return []

        if top_k <= 0:
            raise ValueError(
                "Reranker top_k must be greater than zero."
            )

        question = question.strip()

        logger.info(
            "Starting reranking. Candidates=%d top_k=%d threshold=%.2f",
            len(chunks),
            top_k,
            RerankService.RELEVANCE_THRESHOLD,
        )

        model = CrossEncoderModel.get_model()

        # --------------------------------------------------
        # Normalize chunks
        # --------------------------------------------------

        normalized_chunks = []

        for chunk in chunks:

            if isinstance(chunk, dict):
                normalized = dict(chunk)

            elif hasattr(chunk, "model_dump"):
                normalized = chunk.model_dump()

            elif hasattr(chunk, "dict"):
                normalized = chunk.dict()

            else:
                normalized = {
                    "chunk_id": getattr(
                        chunk,
                        "chunk_id",
                        None,
                    ),
                    "text": getattr(
                        chunk,
                        "text",
                        "",
                    ),
                    "document_name": getattr(
                        chunk,
                        "document_name",
                        "Unknown",
                    ),
                    "page_number": getattr(
                        chunk,
                        "page_number",
                        None,
                    ),
                    "chunk_index": getattr(
                        chunk,
                        "chunk_index",
                        None,
                    ),
                    "distance": getattr(
                        chunk,
                        "distance",
                        None,
                    ),
                }

            if not normalized.get("text"):
                continue

            normalized_chunks.append(normalized)

        if not normalized_chunks:
            logger.warning(
                "No valid chunks available for reranking."
            )
            return []

        # --------------------------------------------------
        # Cross Encoder scoring
        # --------------------------------------------------

        pairs = [
            (
                question,
                chunk["text"],
            )
            for chunk in normalized_chunks
        ]

        logger.debug(
            "Running Cross Encoder prediction. Pairs=%d",
            len(pairs),
        )

        try:
            scores = model.predict(pairs)

        except Exception:
            logger.exception(
                "Cross Encoder prediction failed."
            )
            raise

        # --------------------------------------------------
        # Attach scores
        # --------------------------------------------------

        for chunk, score in zip(
            normalized_chunks,
            scores,
        ):
            chunk["rerank_score"] = float(score)

        # --------------------------------------------------
        # Sort by relevance
        # --------------------------------------------------

        normalized_chunks.sort(
            key=lambda chunk: chunk.get(
                "rerank_score",
                float("-inf"),
            ),
            reverse=True,
        )

        # --------------------------------------------------
        # Relevance filtering
        # --------------------------------------------------

        relevant_chunks = [
            chunk
            for chunk in normalized_chunks
            if chunk.get(
                "rerank_score",
                float("-inf"),
            ) >= RerankService.RELEVANCE_THRESHOLD
        ]

        filtered_count = (
            len(normalized_chunks)
            - len(relevant_chunks)
        )

        logger.info(
            "Reranking relevance filter. "
            "Before=%d Relevant=%d Filtered=%d Threshold=%.2f",
            len(normalized_chunks),
            len(relevant_chunks),
            filtered_count,
            RerankService.RELEVANCE_THRESHOLD,
        )

        # --------------------------------------------------
        # Top-K after relevance filtering
        # --------------------------------------------------

        results = relevant_chunks[:top_k]

        logger.info(
            "Reranking completed. "
            "Candidates=%d Selected=%d",
            len(normalized_chunks),
            len(results),
        )

        return results