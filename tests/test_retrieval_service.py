from src.retrieval.retrieval_service import RetrievalService

response = RetrievalService.search(
    "What is Salesforce?",
    k=3
)

print(response.model_dump())