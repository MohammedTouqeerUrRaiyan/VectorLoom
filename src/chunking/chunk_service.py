from src.chunking.chunker import Chunker
from src.embeddings.embedding_service import EmbeddingService


class ChunkService:

    @staticmethod
    def process(document):

        # 1. Split already-cleaned document text
        chunks = Chunker.split(document)

        # 2. Generate embeddings
        chunks = EmbeddingService.embed_chunks(
            chunks
        )

        return chunks