from fastapi import APIRouter, UploadFile, File

from src.services.file_service import FileService
from src.schemas.upload_schema import UploadResponse

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(file: UploadFile = File(...)):

    saved_path = await FileService.save(file)

    return UploadResponse(

        status="Uploaded",

        filename=file.filename,

        content_type=file.content_type,

        size=saved_path.stat().st_size,

        location=str(saved_path)

    )