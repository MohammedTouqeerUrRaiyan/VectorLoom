from src.embeddings.embedding_model import EmbeddingModel
from src.embeddings.embedding_schema import Embedding


class EmbeddingService:

    @staticmethod
    def create_embeddings(chunks):

        model = EmbeddingModel.get_model()

        texts = [
            chunk.text
            for chunk in chunks
        ]

        vectors = model.encode(
            texts,
            normalize_embeddings=True
        )

        embeddings = []

        for chunk, vector in zip(chunks, vectors):

            embeddings.append(

                Embedding(

                    chunk_id=chunk.chunk_id,

                    vector=vector.tolist(),

                    metadata=chunk.metadata

                )

            )

        return embeddings