from pydantic import BaseModel


class UploadResponse(BaseModel):

    status: str
    filename: str
    content_type: str
    size: int
    location: str