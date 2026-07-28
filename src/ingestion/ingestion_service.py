from pathlib import Path

from src.ingestion.document_loader import DocumentLoader
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.models import Document


class IngestionService:
    """
    Orchestrates the document ingestion pipeline.
    """

    @staticmethod
    def process(file_path: Path) -> Document:
        """
        Processes a document and returns a standardized
        Document object.
        """

        # ----------------------------------------
        # Extract metadata
        # ----------------------------------------

        metadata = MetadataExtractor.extract(file_path)

        # ----------------------------------------
        # Load document
        # ----------------------------------------

        text, pages = DocumentLoader.load(file_path)

        # ----------------------------------------
        # Create standardized document
        # ----------------------------------------

        document = Document(

            filename=metadata["filename"],

            extension=metadata["extension"],

            pages=pages,

            characters=len(text),

            text=text,

            metadata=metadata

        )

        return document