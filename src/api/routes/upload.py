from fastapi import APIRouter, UploadFile, File

from src.chunking.chunk_service import ChunkService
from src.ingestion.ingestion_service import IngestionService
from src.schemas.upload_schema import UploadResponse
from src.services.file_service import FileService
from src.vector_store.store_service import StoreService


router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):

    # 1. Save uploaded file
    saved_path = await FileService.save(file)

    # 2. Ingest document
    document = IngestionService.process(
        saved_path
    )

    # 3. Chunk + generate embeddings
    chunks = ChunkService.process(
        document
    )

    # 4. Store chunks and embeddings
    StoreService.add(
        chunks
    )

    # 5. Return upload response
    return UploadResponse(
        status="Uploaded",
        document=document,
        chunks_created=len(chunks),
        message="Document processed successfully.",
    )