from src.vector_store.chroma_store import ChromaStore


class StoreService:

    _store = ChromaStore()

    @classmethod
    def add(cls, chunks):

        cls._store.add_documents(chunks)

    @classmethod
    def search(cls, embedding, k=5):

        return cls._store.similarity_search(
            embedding,
            k
        )

    @classmethod
    def delete(cls, document_name):

        cls._store.delete_document(document_name)