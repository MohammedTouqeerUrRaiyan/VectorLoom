from src.retrieval.retriever import Retriever
from src.retrieval.retrieval_models import (
    RetrievedChunk,
    RetrievalResponse,
)


class RetrievalService:
    """
    Converts raw ChromaDB results into
    application-friendly response models.
    """

    @staticmethod
    def search(query: str, k: int = 5) -> RetrievalResponse:

        results = Retriever.retrieve(query, k)

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        chunks = []

        for chunk_id, text, meta, distance in zip(
            ids,
            docs,
            metas,
            distances
        ):

            chunks.append(

                RetrievedChunk(

                    chunk_id=chunk_id,

                    document_name=meta["document_name"],

                    page_number=meta["page"],

                    chunk_index=meta["chunk_index"],

                    text=text,

                    distance=distance

                )

            )

        return RetrievalResponse(

            query=query,

            total_results=len(chunks),

            chunks=chunks

        )