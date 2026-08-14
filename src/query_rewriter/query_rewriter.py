import logging

from src.memory.memory_service import MemoryService
from src.llm.llm_service import LLMService


logger = logging.getLogger(__name__)


class QueryRewriter:

    @staticmethod
    def rewrite(
        session_id: str,
        question: str,
    ) -> str:

        question = question.strip()

        if not question:
            return question

        history = MemoryService.history(session_id)

        if not history:
            return question

        # --------------------------------------------------
        # Build only relevant previous conversation
        # --------------------------------------------------

        previous_user_question = None

        for message in reversed(history):

            if message.role == "user":
                previous_user_question = message.content
                break

        if not previous_user_question:
            return question

        # --------------------------------------------------
        # Ask the LLM for a standalone query
        # --------------------------------------------------

        prompt = f"""
You are a query rewriting component in a Retrieval-Augmented
Generation system.

Your ONLY task is to rewrite the CURRENT QUESTION into a
standalone search query when the current question depends
on the PREVIOUS QUESTION.

PREVIOUS QUESTION:
{previous_user_question}

CURRENT QUESTION:
{question}

Rules:

1. Return ONLY the rewritten search query.
2. Do not answer the question.
3. Do not explain your reasoning.
4. Do not ask the user anything.
5. Do not say "can you rephrase".
6. Do not change the meaning of the question.
7. If the current question is already standalone, return it unchanged.
8. Preserve important entity names exactly.
9. Never add information that is not present in the conversation.

Examples:

Previous:
What is VectorLoom?

Current:
What does it use for storage?

Output:
What storage system does VectorLoom use?

Previous:
What is VectorLoom?

Current:
What is Salesforce?

Output:
What is Salesforce?

Previous:
What is VectorLoom?

Current:
Tell me about it.

Output:
Tell me about VectorLoom.

CURRENT QUESTION:
{question}
""".strip()

        try:
            rewritten = LLMService.generate(prompt).strip()

        except Exception:
            logger.exception(
                "Query rewriting failed. "
                "Falling back to original question."
            )

            return question

        # --------------------------------------------------
        # Safety checks
        # --------------------------------------------------

        if not rewritten:
            return question

        # Reject obvious meta-responses from the LLM.
        invalid_prefixes = (
            "can you rephrase",
            "is it possible to rephrase",
            "i can rephrase",
            "here is the rewritten",
            "sure,",
        )

        lowered = rewritten.lower()

        if lowered.startswith(invalid_prefixes):
            logger.warning(
                "Invalid query rewrite detected. "
                "Using original question."
            )

            return question

        logger.info(
            "Query rewrite successful. original=%r rewritten=%r",
            question,
            rewritten,
        )

        return rewritten