from pathlib import Path
from typing import List, Tuple
import fitz


class PDFLoader:
    """
    PDF Loader supporting both:
    1. Loading from a file path
    2. Loading directly from bytes
    """

    @staticmethod
    def load(file_path: Path) -> Tuple[str, int]:
        """
        Used by the Ingestion Pipeline.
        """

        document = fitz.open(file_path)

        pages = len(document)

        extracted_text = []

        for page in document:
            extracted_text.append(page.get_text())

        document.close()

        return "\n".join(extracted_text), pages

    @staticmethod
    def load_from_bytes(file_bytes: bytes) -> List[str]:
        """
        Used for API uploads directly from memory.
        """

        pages = []

        with fitz.open(stream=file_bytes, filetype="pdf") as document:

            for page in document:
                pages.append(page.get_text())

        return pages