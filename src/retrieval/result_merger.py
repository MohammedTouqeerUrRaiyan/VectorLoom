from collections import OrderedDict

from src.logging.logger import setup_logger

logger = setup_logger(__name__)


class ResultMerger:
    """
    Merges vector-search and BM25 results.

    Duplicate chunks are identified using chunk_id.

    Vector results are inserted first so that their metadata
    is preserved when the same chunk is also returned by BM25.
    """

    @staticmethod
    def merge(
        vector_results,
        bm25_results,
    ) -> list[dict]:
        """
        Merge vector and BM25 retrieval results.

        Args:
            vector_results: Raw ChromaDB result dictionary.
            bm25_results: List of RetrievedChunk objects.

        Returns:
            Deduplicated list of normalized chunk dictionaries.
        """

        merged = OrderedDict()

        # --------------------------------------------------
        # VECTOR RESULTS
        # --------------------------------------------------

        if vector_results:
            ids = vector_results.get("ids", [[]])
            documents = vector_results.get("documents", [[]])
            metadatas = vector_results.get("metadatas", [[]])
            distances = vector_results.get("distances", [[]])

            ids = ids[0] if ids else []
            documents = documents[0] if documents else []
            metadatas = metadatas[0] if metadatas else []
            distances = distances[0] if distances else []

            for chunk_id, text, metadata, distance in zip(
                ids,
                documents,
                metadatas,
                distances,
            ):
                if not chunk_id:
                    continue

                metadata = metadata or {}

                merged[chunk_id] = {
                    "chunk_id": chunk_id,
                    "text": text or "",
                    "document_name": metadata.get(
                        "document_name",
                        "Unknown",
                    ),
                    "page_number": metadata.get(
                        "page"
                    ),
                    "chunk_index": metadata.get(
                        "chunk_index"
                    ),
                    "distance": distance,
                    "source": "vector",
                }

        # --------------------------------------------------
        # BM25 RESULTS
        # --------------------------------------------------

        for chunk in bm25_results or []:

            chunk_id = getattr(
                chunk,
                "chunk_id",
                None,
            )

            if not chunk_id:
                continue

            # Don't overwrite vector result.
            if chunk_id in merged:
                continue

            merged[chunk_id] = {
                "chunk_id": chunk_id,
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
                "distance": None,
                "source": "bm25",
            }

        results = list(merged.values())

        logger.info(
            "Result merging complete. "
            "Vector=%d, BM25=%d, Merged=%d",
            ResultMerger._count_vector_results(vector_results),
            len(bm25_results or []),
            len(results),
        )

        return results

    @staticmethod
    def _count_vector_results(vector_results) -> int:
        """
        Safely count vector-search results.
        """

        try:
            return len(
                vector_results.get(
                    "ids",
                    [[]],
                )[0]
            )
        except (
            AttributeError,
            IndexError,
            TypeError,
        ):
            return 0