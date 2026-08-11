from pathlib import Path

from src.ingestion.document import Document
from src.ingestion.pipeline import IngestionPipeline


class IngestionService:
    """
    Orchestrates document ingestion.
    """

    _pipeline = IngestionPipeline()

    @classmethod
    def process(cls, file_path):

        file_path = Path(file_path)

        return cls._pipeline.run(file_path)