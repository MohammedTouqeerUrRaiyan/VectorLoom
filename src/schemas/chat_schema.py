from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question",
    )

    session_id: str = Field(
        default="default",
        description="Conversation session identifier",
    )


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]