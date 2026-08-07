from src.chunking.chunk_models import Chunk

from src.retrieval.hybrid_retriever import HybridRetriever

from src.retrieval.result_merger import ResultMerger


chunks = [

    Chunk(
        chunk_id="1",
        document_name="Salesforce.pdf",
        page_number=1,
        chunk_index=0,
        text="Salesforce CRM",
        character_count=20,
        metadata={}
    ),

    Chunk(
        chunk_id="2",
        document_name="Apex.pdf",
        page_number=1,
        chunk_index=0,
        text="Apex language",
        character_count=20,
        metadata={}
    )

]

retriever = HybridRetriever()

vector_results, bm25_results = retriever.search(
    "Salesforce",
    chunks
)

merged = ResultMerger.merge(
    vector_results,
    bm25_results
)

print()

print("Merged")

print()

for item in merged:

    print(item["document_name"])