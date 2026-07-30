from pydantic import BaseModel, Field
from typing import Dict


class Chunk(BaseModel):
    """
    Standard chunk model used throughout VectorLoom.
    """

    chunk_id: str = Field(
        description="Unique identifier for the chunk"
    )

    document_name: str = Field(
        description="Original document filename"
    )

    page_number: int = Field(
        default=1,
        description="Page number from which the chunk originated"
    )

    chunk_index: int = Field(
        description="Sequential chunk number"
    )

    text: str = Field(
        description="Chunk text"
    )

    character_count: int = Field(
        description="Number of characters in this chunk"
    )

    metadata: Dict = Field(
        default_factory=dict,
        description="Additional metadata"
    )