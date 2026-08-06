from typing import List
from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    chunk_id: str
    document_name: str
    page_number: int
    chunk_index: int
    text: str
    distance: float


class RetrievalResponse(BaseModel):
    query: str
    total_results: int
    chunks: List[RetrievedChunk]