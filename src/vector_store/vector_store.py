from abc import ABC, abstractmethod


class VectorStore(ABC):

    @abstractmethod
    def add_documents(self, chunks):
        pass

    @abstractmethod
    def similarity_search(self, query_embedding, k=5):
        pass

    @abstractmethod
    def delete_document(self, document_name):
        pass