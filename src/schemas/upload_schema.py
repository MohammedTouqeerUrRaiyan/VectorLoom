from pydantic import BaseModel

from src.ingestion.models import Document


class UploadResponse(BaseModel):

    status: str

    document: Document