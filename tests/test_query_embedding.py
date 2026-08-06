from src.retrieval.query_embedder import QueryEmbedder

query = "Explain Salesforce Profiles"

embedding = QueryEmbedder.embed(query)

print(type(embedding))
print(len(embedding))
print(embedding[:5])