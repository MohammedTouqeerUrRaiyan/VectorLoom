from src.memory.memory_service import MemoryService


class PromptBuilder:
    """
    Builds the final RAG prompt using:
    - conversation history
    - retrieved document chunks
    - current user question
    """

    @staticmethod
    def build(
        session_id: str,
        question: str,
        chunks: list,
    ) -> str:

        # ----------------------------------------
        # Conversation history
        # ----------------------------------------

        history = MemoryService.history(session_id)

        history_text = "\n".join(
            f"{message.role}: {message.content}"
            for message in history
        )

        if not history_text:
            history_text = "No previous conversation."

        # ----------------------------------------
        # Retrieved document context
        # ----------------------------------------

        context_parts = []

        for chunk in chunks:

            if isinstance(chunk, dict):
                text = chunk.get("text", "")
                document_name = chunk.get(
                    "document_name",
                    "Unknown",
                )
                page_number = chunk.get(
                    "page_number",
                    0,
                )

            else:
                text = getattr(
                    chunk,
                    "text",
                    "",
                )
                document_name = getattr(
                    chunk,
                    "document_name",
                    "Unknown",
                )
                page_number = getattr(
                    chunk,
                    "page_number",
                    0,
                )

            if not text:
                continue

            context_parts.append(
                f"Document: {document_name}\n"
                f"Page: {page_number}\n"
                f"Content:\n{text}"
            )

        context = "\n\n---\n\n".join(context_parts)

        if not context:
            context = "No relevant document context was retrieved."

        # ----------------------------------------
        # Final RAG prompt
        # ----------------------------------------

        return f"""
You are VectorLoom, an enterprise Retrieval-Augmented Generation (RAG) assistant.

STRICT RULES:

1. Answer ONLY using information contained in DOCUMENT CONTEXT.

2. CONVERSATION HISTORY may ONLY be used to understand references
   such as:
   - it
   - they
   - this
   - that
   - he
   - she

3. Never use your own knowledge.

4. Never invent, assume, or infer facts that are not explicitly supported
   by DOCUMENT CONTEXT.

5. If the answer cannot be found in DOCUMENT CONTEXT, reply exactly:

I couldn't find that information in the uploaded documents.

6. Do NOT mention document names, page numbers, citations, or references
   in your answer.

7. Do NOT output labels such as:
   - Document:
   - Page:
   - References:
   - Sources:
   - Answer:

8. Do NOT explain your reasoning.

9. Do NOT mention the DOCUMENT CONTEXT or CONVERSATION HISTORY
   in the final answer.

10. Keep the answer concise and directly answer the user's question.

11. The application will add document citations and references separately.
    Therefore, NEVER generate citations yourself.

---

CONVERSATION HISTORY

{history_text}

---

DOCUMENT CONTEXT

{context}

---

QUESTION

{question}

---

ANSWER
""".strip()