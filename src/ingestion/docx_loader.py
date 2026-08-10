from pathlib import Path
from docx import Document


class DocxLoader:
    @staticmethod
    def load(file_path: Path) -> tuple[str, int]:
        document = Document(file_path)

        full_text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)

        text = "\n".join(full_text)

        # python-docx does not provide physical page counts.
        # Treat the document as one logical page.
        pages = 1

        return text, pages
