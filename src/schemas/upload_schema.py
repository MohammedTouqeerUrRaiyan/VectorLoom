from pydantic import BaseModel, Field

from src.ingestion.models import Document


class UploadResponse(BaseModel):
    """
    Standard response returned after a document upload.
    """

    status: str = Field(
        ...,
        description="Overall upload status."
    )

    document: Document = Field(
        ...,
        description="Processed document information."
    )

    chunks_created: int = Field(
        ...,
        ge=0,
        description="Total number of chunks generated from the document."
    )

    message: str = Field(
        default="Document processed successfully.",
        description="Human-readable status message."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Uploaded",
                "message": "Document processed successfully.",
                "chunks_created": 42,
                "document": {
                    "filename": "Salesforce_Admin_Guide.pdf",
                    "extension": ".pdf",
                    "pages": 38,
                    "characters": 125643,
                    "text": "Extracted document text...",
                    "metadata": {
                        "filename": "Salesforce_Admin_Guide.pdf",
                        "extension": ".pdf",
                        "size": 5686699,
                        "created_at": "2026-08-04T12:10:33"
                    }
                }
            }
        }