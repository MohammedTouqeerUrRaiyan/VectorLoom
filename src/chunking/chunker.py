from src.chunking.recursive_chunker import RecursiveChunker


class Chunker:

    @staticmethod
    def split(document):

        return RecursiveChunker.split(document)