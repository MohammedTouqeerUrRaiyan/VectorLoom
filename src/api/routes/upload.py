from fastapi import APIRouter, UploadFile, File
from src.chunking.chunk_service import ChunkService
from src.schemas.upload_schema import UploadResponse
from src.services.file_service import FileService
from src.ingestion.ingestion_service import IngestionService

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(file: UploadFile = File(...)):

    saved_path = await FileService.save(file)

    # Extract document
    document = IngestionService.process(saved_path)

    # Create chunks
    chunks = ChunkService.process(document)

    return UploadResponse(
        status="Uploaded",
        document=document,
        chunks_created=len(chunks)
    )