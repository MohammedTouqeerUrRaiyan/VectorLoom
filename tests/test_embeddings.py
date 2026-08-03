from src.embeddings.embedding_service import EmbeddingService
from src.chunking.chunk_models import Chunk

chunk = Chunk(
    chunk_id="1",
    document_name="sample.pdf",
    page_number=1,
    chunk_index=0,
    text="Salesforce is a CRM platform.",
    character_count=30,
    metadata={}
)

embeddings = EmbeddingService.create_embeddings([chunk])

print(len(embeddings))
print(len(embeddings[0].vector))
print(embeddings[0].vector[:5])