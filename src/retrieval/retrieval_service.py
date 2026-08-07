from src.retrieval.retriever import Retriever
from src.retrieval.retrieval_models import (
    RetrievedChunk,
    RetrievalResponse,
)

from src.logging.logger import setup_logger


logger = setup_logger(__name__)


class RetrievalService:
    """
    Converts raw ChromaDB results into
    application-friendly response models.
    """

    @staticmethod
    def search(
        query: str,
        k: int = 10,
    ) -> RetrievalResponse:

        logger.info(
            "RetrievalService searching. query='%s' k=%d",
            query,
            k,
        )

        results = Retriever.retrieve(
            query,
            k,
        )

        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        chunks = []

        for chunk_id, text, meta, distance in zip(
            ids,
            docs,
            metas,
            distances,
        ):

            chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    document_name=meta.get(
                        "document_name",
                        "Unknown",
                    ),
                    page_number=meta.get(
                        "page",
                        0,
                    ),
                    chunk_index=meta.get(
                        "chunk_index",
                        0,
                    ),
                    text=text,
                    distance=distance,
                )
            )

        logger.info(
            "RetrievalService returned %d chunks",
            len(chunks),
        )

        return RetrievalResponse(
            query=query,
            total_results=len(chunks),
            chunks=chunks,
        )