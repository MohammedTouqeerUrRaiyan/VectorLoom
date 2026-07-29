from pathlib import Path
from docx import Document


class DocxLoader:
    """
    Loads Microsoft Word (.docx) documents.
    """

    @staticmethod
    def load(file_path: Path) -> tuple[str, int]:

        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:
            text.append(paragraph.text)

        full_text = "\n".join(text)

        # DOCX has no real page information
        return full_text, 1