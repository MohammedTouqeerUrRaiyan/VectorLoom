from collections import OrderedDict


class CitationService:
    """
    Builds citations for documents used by the RAG response.
    """

    @staticmethod
    def build(answer: str, chunks: list) -> str:
        """
        Append numbered document references.

        If no chunks are available, return the answer unchanged.
        """

        if not answer:
            return ""

        if not chunks:
            return answer.strip()

        references = OrderedDict()

        for chunk in chunks:

            if isinstance(chunk, dict):
                document = chunk.get("document_name", "Unknown")
                page = chunk.get("page_number", 0)

            else:
                document = getattr(
                    chunk,
                    "document_name",
                    "Unknown",
                )
                page = getattr(
                    chunk,
                    "page_number",
                    0,
                )

            key = (document, page)

            if key not in references:
                references[key] = len(references) + 1

        if not references:
            return answer.strip()

        citation_text = "\n\nReferences\n"

        for (document, page), number in references.items():
            citation_text += (
                f"\n[{number}] {document} (Page {page})"
            )

        return answer.strip() + citation_text