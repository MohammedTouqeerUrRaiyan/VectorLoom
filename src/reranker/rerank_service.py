from src.logging.logger import setup_logger
from src.reranker.cross_encoder import CrossEncoderModel

logger = setup_logger(__name__)


class RerankService:
    """
    Re-ranks retrieved chunks using a Cross Encoder.

    Input chunks may be dictionaries or Pydantic models.
    Output is normalized to dictionaries so it remains
    compatible with ResultMerger and downstream services.
    """

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
            "Starting reranking. Candidates=%d top_k=%d",
            len(chunks),
            top_k,
        )

        model = CrossEncoderModel.get_model()

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

            normalized_chunks.append(
                normalized
            )

        if not normalized_chunks:
            logger.warning(
                "No valid chunks available for reranking."
            )
            return []

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
            scores = model.predict(
                pairs
            )
        except Exception:
            logger.exception(
                "Cross Encoder prediction failed."
            )
            raise

        for chunk, score in zip(
            normalized_chunks,
            scores,
        ):
            chunk["rerank_score"] = float(
                score
            )

        normalized_chunks.sort(
            key=lambda chunk: chunk.get(
                "rerank_score",
                float("-inf"),
            ),
            reverse=True,
        )

        results = normalized_chunks[
            :top_k
        ]

        logger.info(
            "Reranking completed. "
            "Candidates=%d Selected=%d",
            len(normalized_chunks),
            len(results),
        )

        return results