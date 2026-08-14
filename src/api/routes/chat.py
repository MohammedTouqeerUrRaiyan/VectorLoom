import logging
from typing import Any

from fastapi import APIRouter, HTTPException, status

from src.cache.cache_service import CacheService
from src.citation.citation_service import CitationService
from src.llm.llm_service import LLMService
from src.llm.prompt_builder import PromptBuilder
from src.memory.memory_service import MemoryService
from src.query_rewriter.query_rewriter import QueryRewriter
from src.reranker.rerank_service import RerankService
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.result_merger import ResultMerger
from src.retrieval.retrieval_service import RetrievalService
from src.schemas.chat_schema import ChatRequest, ChatResponse


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Execute the VectorLoom RAG pipeline.

    Pipeline:

        User Question
              ↓
        Query Rewriting
              ↓
        Cache Lookup
              ↓
        Vector Retrieval
              ↓
        Hybrid Retrieval
              ↓
        Result Merging
              ↓
        Re-ranking
              ↓
        Prompt Construction
              ↓
        LLM Generation
              ↓
        Citation Generation
              ↓
        Conversation Memory
    """

    session_id = request.session_id
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty.",
        )

    logger.info(
        "Chat request received. session_id=%s question=%r",
        session_id,
        question,
    )

    try:
        # --------------------------------------------------
        # 1. Rewrite query BEFORE storing current message
        # --------------------------------------------------

        rewritten_question = QueryRewriter.rewrite(
            session_id=session_id,
            question=question,
        )

        if not rewritten_question:
            rewritten_question = question

        logger.info(
            "Query rewritten. session_id=%s original=%r rewritten=%r",
            session_id,
            question,
            rewritten_question,
        )

        # --------------------------------------------------
        # 2. Cache lookup
        # --------------------------------------------------

        best_chunks = CacheService.get(rewritten_question)

        if best_chunks:
            logger.info(
                "Cache hit. session_id=%s chunks=%d",
                session_id,
                len(best_chunks),
            )

        else:
            logger.info(
                "Cache miss. Starting retrieval pipeline. "
                "session_id=%s",
                session_id,
            )

            # --------------------------------------------------
            # 3. Initial semantic retrieval
            # --------------------------------------------------

            retrieval = RetrievalService.search(
                rewritten_question,
                k=10,
            )

            candidate_chunks = retrieval.chunks

            if not candidate_chunks:
                logger.warning(
                    "No retrieval candidates found. "
                    "session_id=%s query=%r",
                    session_id,
                    rewritten_question,
                )

                best_chunks = []

            else:
                # --------------------------------------------------
                # 4. Hybrid retrieval
                # --------------------------------------------------

                hybrid_retriever = HybridRetriever()

                vector_results, bm25_results = (
                    hybrid_retriever.search(
                        question=rewritten_question,
                        chunks=candidate_chunks,
                        top_k=10,
                    )
                )

                # --------------------------------------------------
                # 5. Merge vector + BM25 results
                # --------------------------------------------------

                merged_chunks = ResultMerger.merge(
                    vector_results=vector_results,
                    bm25_results=bm25_results,
                )

                if not merged_chunks:
                    logger.warning(
                        "Hybrid retrieval returned no results. "
                        "session_id=%s",
                        session_id,
                    )

                    best_chunks = []

                else:
                    # --------------------------------------------------
                    # 6. Cross-encoder reranking
                    # --------------------------------------------------

                    best_chunks = RerankService.rerank(
                        question=rewritten_question,
                        chunks=merged_chunks,
                        top_k=5,
                    )

            # --------------------------------------------------
            # 7. Cache only useful results
            # --------------------------------------------------

            if best_chunks:
                CacheService.set(
                    key=rewritten_question,
                    value=best_chunks,
                )

        # --------------------------------------------------
        # 8. Build grounded prompt
        # --------------------------------------------------

        prompt = PromptBuilder.build(
            session_id=session_id,
            question=question,
            chunks=best_chunks,
        )

        # --------------------------------------------------
        # 9. Generate LLM response
        # --------------------------------------------------

        raw_answer = LLMService.generate(prompt)

        if not raw_answer:
            logger.error(
                "LLM returned an empty response. session_id=%s",
                session_id,
            )

            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The language model returned an empty response.",
            )

        # --------------------------------------------------
        # 10. Add citations
        # --------------------------------------------------

        answer = CitationService.build(
            answer=raw_answer,
            chunks=best_chunks,
        )

        # --------------------------------------------------
        # 11. Persist conversation
        #
        # IMPORTANT:
        # Store the current user message AFTER query rewriting.
        # Otherwise the current question becomes "history".
        # --------------------------------------------------

        MemoryService.add_user_message(
            session_id=session_id,
            content=question,
        )

        MemoryService.add_assistant_message(
            session_id=session_id,
            content=answer,
        )

        # --------------------------------------------------
        # 12. Build unique source list
        # --------------------------------------------------

        sources = _extract_sources(best_chunks)

        logger.info(
            "Chat request completed. session_id=%s sources=%d",
            session_id,
            len(sources),
        )

        return ChatResponse(
            question=question,
            answer=answer,
            sources=sources,
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while processing chat request. "
            "session_id=%s",
            session_id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request.",
        )


def _extract_sources(chunks: list[Any]) -> list[str]:
    """
    Extract unique document names from retrieved chunks.

    Supports both dictionaries and Pydantic/model objects.
    """

    sources: set[str] = set()

    for chunk in chunks:
        if isinstance(chunk, dict):
            document_name = chunk.get("document_name")
        else:
            document_name = getattr(
                chunk,
                "document_name",
                None,
            )

        if document_name:
            sources.add(document_name)

    return sorted(sources)