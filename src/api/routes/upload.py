from fastapi import APIRouter, UploadFile, File
from src.schemas.upload_schema import UploadResponse
from src.services.file_service import FileService
from src.schemas.upload_schema import UploadResponse

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(file: UploadFile = File(...)):

    saved_path = await FileService.save(file)

    document = IngestionService.process(saved_path)

    return UploadResponse(

        status="Uploaded",

        document=document

    )