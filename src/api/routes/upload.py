from fastapi import APIRouter, UploadFile, File

from src.chunking.chunk_service import ChunkService
from src.embeddings.embedding_service import EmbeddingService
from src.ingestion.ingestion_service import IngestionService
from src.schemas.upload_schema import UploadResponse
from src.services.file_service import FileService
from src.vector_store.store_service import StoreService

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(file: UploadFile = File(...)):

    saved_path = await FileService.save(file)

    # Extract document
    document = IngestionService.process(saved_path)

    chunks = ChunkService.process(document)

    EmbeddingService.embed_chunks(chunks)

    StoreService.add(chunks)



    return UploadResponse(
        status="Uploaded",
        document=document,
        chunks_created=len(chunks),
        message="Document processed successfully."
    )