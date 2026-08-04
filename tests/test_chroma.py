from chromadb import PersistentClient

client = PersistentClient(path="data/chroma_db")
collection = client.get_collection("vectorloom")

print("Documents:", collection.count())