from chromadb import PersistentClient

from src.vector_store.vector_store import VectorStore


class ChromaStore(VectorStore):

    def __init__(self):

        self.client = PersistentClient(path="data/chroma_db")

        self.collection = self.client.get_or_create_collection(
            name="vectorloom"
        )

    def add_documents(self, chunks):

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(chunk.chunk_id)

            embeddings.append(chunk.embedding)

            documents.append(chunk.text)

            metadatas.append(
                {
                    "document_name": chunk.document_name,
                    "page": chunk.page_number,
                    "chunk_index": chunk.chunk_index
                }
            )

        self.collection.add(

            ids=ids,

            embeddings=embeddings,

            documents=documents,

            metadatas=metadatas

        )

    def similarity_search(self, query_embedding, k=5):

        results = self.collection.query(

            query_embeddings=[query_embedding],

            n_results=k

        )

        return results

    def delete_document(self, document_name):

        self.collection.delete(

            where={
                "document_name": document_name
            }

        )