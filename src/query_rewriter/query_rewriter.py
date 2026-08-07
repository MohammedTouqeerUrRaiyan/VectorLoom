from src.memory.memory_service import MemoryService


class QueryRewriter:

    @staticmethod
    def rewrite(
        session_id: str,
        question: str
    ) -> str:

        history = MemoryService.history(session_id)

        if not history:
            return question

        previous_user = None

        for message in reversed(history):

            if message.role == "user":

                previous_user = message.content

                break

        if previous_user is None:
            return question

        prompt = f"""
Conversation

Previous question:
{previous_user}

Current question:
{question}

Rewrite the current question into a complete standalone question.

Only return the rewritten question.

If no rewrite is needed,
return the original question.
"""

        from src.llm.llm_service import LLMService

        return LLMService.generate(prompt).strip()