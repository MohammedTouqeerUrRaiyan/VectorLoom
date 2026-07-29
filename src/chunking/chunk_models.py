from pydantic import BaseModel
from typing import Dict


class Chunk(BaseModel):
    chunk_id: str
    document_name: str
    page_number: int
    text: str
    character_count: int
    metadata: Dict