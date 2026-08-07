from src.chunking.chunk_models import Chunk
from src.retrieval.bm25 import BM25Retriever

chunks = [

    Chunk(
        chunk_id="1",
        document_name="Salesforce.pdf",
        page_number=1,
        chunk_index=0,
        text="Salesforce is a CRM platform",
        character_count=28,
        metadata={}
    ),

    Chunk(
        chunk_id="2",
        document_name="Apex.pdf",
        page_number=1,
        chunk_index=0,
        text="Apex is Salesforce programming language",
        character_count=40,
        metadata={}
    )

]

retriever = BM25Retriever()

retriever.build_index(chunks)

results = retriever.search(
    "Salesforce CRM",
    top_k=2
)

for chunk in results:
    print(chunk.document_name)
    print(chunk.text)
    print("--------")