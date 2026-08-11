from fastapi import APIRouter

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

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Log user message immediately to guarantee complete conversation history
    MemoryService.add_user_message(
        session_id=request.session_id,
        content=request.question
    )

    # Contextual query rewriter
    rewritten_question = QueryRewriter.rewrite(
        session_id=request.session_id, question=request.question
    )

    # 2. Check cache using rewritten query
    cached_chunks = CacheService.get(rewritten_question)

    if cached_chunks:
        best_chunks = cached_chunks
    else:
        # Fetch candidate chunks from retrieval pipeline
        retrieval = RetrievalService.search(rewritten_question)

        # Hybrid Retrieval (Vector + BM25 Keyword)
        retriever = HybridRetriever()
        vector_results, bm25_results = retriever.search(
            question=rewritten_question, chunks=retrieval.chunks, top_k=10
        )

        # Merge Results
        merged = ResultMerger.merge(
            vector_results=vector_results, bm25_results=bm25_results
        )

        # Re-rank Chunks using the contextual query
        best_chunks = RerankService.rerank(
            question=rewritten_question, chunks=merged, top_k=5
        )

        # Cache top chunks under the rewritten key
        CacheService.set(key=rewritten_question, value=best_chunks)

    # 3. Build Prompt with session history & relevant chunks
    prompt = PromptBuilder.build(
        session_id=request.session_id,
        question=request.question,
        chunks=best_chunks,
    )

    # 4. Generate Response with LLM
    raw_answer = LLMService.generate(prompt)

    # 5. Format & Append Citations
    answer = CitationService.build(answer=raw_answer, chunks=best_chunks)

    # 6. Log Assistant response to session history
    MemoryService.add_assistant_message(
        session_id=request.session_id,
        content=answer
    )

    # 7. Deduplicate Sources safely
    sources = list(
        {
            (
                chunk.get("document_name")
                if isinstance(chunk, dict)
                else getattr(chunk, "document_name", "Unknown")
            )
            for chunk in best_chunks
        }
    )

    return ChatResponse(
        question=request.question, answer=answer, sources=sources
    )