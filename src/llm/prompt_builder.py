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

1. Answer ONLY using the supplied DOCUMENT CONTEXT.

2. Use CONVERSATION HISTORY only to understand references such as:
   - it
   - they
   - this
   - that
   - he
   - she

3. Never answer using your own knowledge.

4. Never invent facts.

5. If the answer cannot be found in the DOCUMENT CONTEXT, reply exactly:

I couldn't find that information in the uploaded documents.

6. Always mention the document names used to answer the question.

7. Do not use information from previous conversation messages as factual evidence.

8. Keep the answer concise and directly answer the user's question.

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