from src.chunking.cleaner import TextCleaner
from src.chunking.chunker import Chunker

from src.embeddings.embedding_service import EmbeddingService


class ChunkService:

    @staticmethod
    def process(document):

        document.text = TextCleaner.clean(
            document.text
        )

        chunks = Chunker.split(document)

        chunks = EmbeddingService.embed_chunks(
            chunks
        )

        return chunks