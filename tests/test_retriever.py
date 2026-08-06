from src.retrieval.retriever import Retriever

query = "What is Salesforce?"

results = Retriever.retrieve(query, k=3)

print(results)