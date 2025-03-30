import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("function_registry")

# Initialize embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Store session history
session_history = []

def retrieve_function(user_query):
    global session_history

    # Add the new query to session history
    session_history.append(user_query)

    # Generate embeddings for all past queries (context-aware retrieval)
    query_embeddings = [embedder.encode(q).tolist() for q in session_history]

    # Search for the best function using all queries in history
    results = collection.query(query_embeddings=query_embeddings, n_results=1)

    if results['ids'][0]:
        return results['metadatas'][0][0]['function']
    
    return None  # No function found
