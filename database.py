from chromadb import ChromaDB

# Initialize ChromaDB with a persistent directory
db = ChromaDB(persist_directory="./chroma_persistent_db")

def add_document(doc_id: str, text: str, embedding: list):
    db.add_document(doc_id=doc_id, text=text, embedding=embedding)

def query_documents(query_embedding: list, top_k: int = 5):
    return db.query_documents(embedding=query_embedding, top_k=top_k)
