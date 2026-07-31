from src.chunking.cleaner import TextCleaner
from src.chunking.chunker import Chunker


class ChunkService:

    @staticmethod
    def process(document):

        document.text = TextCleaner.clean(document.text)

        chunks = Chunker.split(document)

        return chunks