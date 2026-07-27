# src/services/document_service.py

from pathlib import Path


class DocumentService:

    @staticmethod
    def process_document(path: str):

        suffix = Path(path).suffix.lower()

        return {
            "filename": Path(path).name,
            "extension": suffix,
            "message": "Document received successfully."
        }