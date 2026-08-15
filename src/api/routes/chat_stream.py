from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.schemas.chat_schema import ChatRequest
from src.retrieval.retrieval_service import RetrievalService
from src.memory.memory_service import MemoryService
from src.llm.prompt_builder import PromptBuilder
from src.llm.streaming_service import StreamingService

router = APIRouter()


@router.post("/chat-stream")
async def chat_stream(request: ChatRequest):

    session_id = request.session_id

    MemoryService.add_user_message(
        session_id,
        request.question
    )

    retrieval = RetrievalService.search(
        request.question
    )

    prompt = PromptBuilder.build(
        session_id=session_id,
        question=request.question,
        chunks=retrieval.chunks
    )

    return StreamingResponse(
        StreamingService.stream(prompt),
        media_type="text/plain"
    )