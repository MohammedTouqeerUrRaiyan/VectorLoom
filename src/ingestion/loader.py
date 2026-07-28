from pathlib import Path

from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.text_loader import TextLoader


class DocumentLoader:
    """
    Dispatches documents to the appropriate loader
    based on file extension.
    """

    @staticmethod
    def load(file_path: Path) -> tuple[str, int]:

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFLoader.load(file_path)

        elif extension == ".txt":
            return TextLoader.load(file_path)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )