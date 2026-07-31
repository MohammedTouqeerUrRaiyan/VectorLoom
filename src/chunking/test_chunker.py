from src.ingestion.models import Document
from src.chunking.recursive_chunker import RecursiveChunker

doc = Document(

    filename="sample.pdf",

    extension=".pdf",

    pages=1,

    characters=8000,

    text="Hello VectorLoom " * 600,

    metadata={}
)

chunks = RecursiveChunker.split(doc)

print(f"Total Chunks : {len(chunks)}")

print(chunks[0])