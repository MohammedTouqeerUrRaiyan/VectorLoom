class VectorStore:
    """
    Base vector database interface.
    """

    def add(self, chunks):

        raise NotImplementedError

    def search(self, query_vector, top_k=5):

        raise NotImplementedError