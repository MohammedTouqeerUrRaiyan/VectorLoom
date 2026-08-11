from typing import Optional
from pydantic import BaseModel


class Chunk(BaseModel):

    chunk_id: str

    document_name: str

    page_number: int

    chunk_index: int

    text: str

    character_count: int

    metadata: dict

    embedding: list[float] | None = None