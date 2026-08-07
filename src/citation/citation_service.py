from collections import OrderedDict


class CitationService:
    """
    Builds numbered citations and a references section
    for RAG responses.
    """

    @staticmethod
    def build(answer: str, chunks: list) -> str:
        """
        Parameters
        ----------
        answer : str
            LLM generated answer.

        chunks : list
            List of retrieved chunks.

            Each chunk must contain:
                document_name
                page_number

            Works with either dictionaries or Pydantic models.
        """

        references = OrderedDict()

        for chunk in chunks:

            if isinstance(chunk, dict):

                document = chunk["document_name"]
                page = chunk["page_number"]

            else:

                document = chunk.document_name
                page = chunk.page_number

            key = (document, page)

            if key not in references:
                references[key] = len(references) + 1

        citation_text = "\n\nReferences\n"

        for (document, page), number in references.items():

            citation_text += (
                f"\n[{number}] {document} (Page {page})"
            )

        return answer.strip() + citation_text