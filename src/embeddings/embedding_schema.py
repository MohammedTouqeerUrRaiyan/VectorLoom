from pydantic import BaseModel
from typing import List


class Embedding(BaseModel):

    chunk_id: str

    vector: List[float]

    metadata: dict