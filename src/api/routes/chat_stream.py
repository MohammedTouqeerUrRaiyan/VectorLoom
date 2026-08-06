from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.schemas.chat_schema import ChatRequest

from src.retrieval.retrieval_service import RetrievalService
from src.llm.prompt_builder import PromptBuilder
from src.llm.streaming_llm import StreamingLLM

router = APIRouter()


@router.post("/stream")
async def stream_chat(request: ChatRequest):

    retrieved = RetrievalService.retrieve(
        request.question
    )

    prompt = PromptBuilder.build(
        request.question,
        retrieved.chunks
    )

    return StreamingResponse(

        StreamingLLM.generate(prompt),

        media_type="text/plain"

    )