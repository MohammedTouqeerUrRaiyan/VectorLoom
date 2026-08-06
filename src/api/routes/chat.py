from fastapi import APIRouter

from src.llm.llm_models import ChatRequest, ChatResponse
from src.llm.prompt_builder import PromptBuilder
from src.llm.llm_service import LLMService
from src.retrieval.retrieval_service import RetrievalService

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    retrieval = RetrievalService.search(request.question)

    prompt = PromptBuilder.build(
        request.question,
        retrieval.chunks
    )

    answer = LLMService.generate(prompt)

    return ChatResponse(
        question=request.question,
        answer=answer,
        sources=list(
        dict.fromkeys(
            chunk.document_name
            for chunk in retrieval.chunks
        )
    )
    )