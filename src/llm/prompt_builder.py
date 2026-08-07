from src.memory.memory_service import MemoryService
from src.memory.memory_service import MemoryService

class PromptBuilder:

    @staticmethod
    def build(
        session_id: str,
        question: str,
        chunks
    ):

        history = MemoryService.get_history(session_id)

        history_text = ""

        for message in history:

            history_text += (
                f"{message.role}: {message.content}\n"
            )

        context = "\n\n".join(
            chunk["text"]
            for chunk in chunks
        )

        return f"""
You are VectorLoom, an enterprise Retrieval-Augmented Generation (RAG) assistant.

STRICT RULES:

1. Answer ONLY using the supplied CONTEXT.

2. Use the CONVERSATION HISTORY only to understand references such as:
   - it
   - they
   - this
   - that
   - he
   - she

3. Never answer using your own knowledge.

4. Never invent facts.

5. If the answer is missing from the context, reply exactly:

I couldn't find that information in the uploaded documents.

6. Always mention the document names you used.

----------------------------------------
CONVERSATION HISTORY

{history_text}

----------------------------------------
DOCUMENT CONTEXT

{context}

----------------------------------------
QUESTION

{question}

----------------------------------------
ANSWER
"""