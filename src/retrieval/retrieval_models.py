from typing import List, Optional

from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    """
    Normalized representation of a retrieved document chunk.
    """

    chunk_id: str
    document_name: str
    page_number: Optional[int] = None
    chunk_index: Optional[int] = None
    text: str

    # Vector distance is unavailable for BM25-only results.
    distance: Optional[float] = None

    # Retrieval/reranking metadata.
    source: Optional[str] = None
    rerank_score: Optional[float] = None


class RetrievalResponse(BaseModel):
    """
    Response returned by the retrieval service.
    """

    query: str
    total_results: int = Field(ge=0)
    chunks: List[RetrievedChunk]