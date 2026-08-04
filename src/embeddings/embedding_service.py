from typing import List

from src.embeddings.embedding_model import EmbeddingModel
from src.embeddings.embedding_schema import Embedding
from src.chunking.chunk_models import Chunk


class EmbeddingService:
    """
    Handles embedding generation for VectorLoom.
    """

    _model = None

    @classmethod
    def get_model(cls):
        """
        Load the embedding model only once.
        """
        if cls._model is None:
            cls._model = EmbeddingModel.get_model()
        return cls._model

    @classmethod
    def embed(cls, text: str) -> list[float]:
        """
        Generate embedding for a single text.
        """
        model = cls.get_model()

        vector = model.encode(
            text,
            normalize_embeddings=True
        )

        return vector.tolist()

    @classmethod
    def embed_chunks(cls, chunks: List[Chunk]) -> List[Chunk]:
        """
        Generate embeddings for every chunk.
        """

        if not chunks:
            return chunks

        model = cls.get_model()

        texts = [chunk.text for chunk in chunks]

        vectors = model.encode(
            texts,
            normalize_embeddings=True
        )

        for chunk, vector in zip(chunks, vectors):
            chunk.embedding = vector.tolist()

        return chunks

    @staticmethod
    def create_embeddings(chunks: List[Chunk]) -> List[Embedding]:
        """
        Convert chunk objects into Embedding schema objects.
        """

        embeddings = []

        for chunk in chunks:

            embeddings.append(
                Embedding(
                    chunk_id=chunk.chunk_id,
                    vector=chunk.embedding,
                    metadata=chunk.metadata
                )
            )

        return embeddings