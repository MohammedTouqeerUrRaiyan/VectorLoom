from src.chunking.chunk_models import Chunk
from src.retrieval.hybrid_retriever import HybridRetriever

chunks = [

    Chunk(
        chunk_id="1",
        document_name="Salesforce.pdf",
        page_number=1,
        chunk_index=0,
        text="Salesforce is a CRM platform.",
        character_count=28,
        metadata={}
    ),

    Chunk(
        chunk_id="2",
        document_name="Apex.pdf",
        page_number=1,
        chunk_index=0,
        text="Apex is Salesforce programming language.",
        character_count=40,
        metadata={}
    )

]

retriever = HybridRetriever()

vector_results, bm25_results = retriever.search(
    "Salesforce CRM",
    chunks,
    top_k=2
)

print("Vector Search")
print(vector_results)

print()

print("BM25 Search")

for chunk in bm25_results:
    print(chunk.document_name)