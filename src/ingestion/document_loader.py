from pathlib import Path

from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.text_loader import TextLoader
from src.ingestion.docx_loader import DocxLoader
from src.ingestion.image_loader import ImageLoader


class DocumentLoader:

    @staticmethod
    def load(file_path: Path):

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFLoader.load(file_path)

        elif extension == ".txt":
            return TextLoader.load(file_path)

        elif extension == ".docx":
            return DocxLoader.load(file_path)

        elif extension in [".png", ".jpg", ".jpeg"]:
            return ImageLoader.load(file_path)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )