import chromadb
from sentence_transformers import SentenceTransformer
from custom_functions import custom_functions  # Import custom functions

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("function_registry")

# Initialize embedding model (using a lightweight open source model)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Predefined function metadata (Function name: Description)
functions = {
    "open_chrome": "Open Google Chrome browser",
    "open_calculator": "Open Calculator application",
    "open_notepad": "Open Notepad application",
    "open_file_explorer": "Open File Explorer",
    "get_cpu_usage": "Retrieve current CPU usage",
    "get_ram_usage": "Retrieve current RAM usage",
    "run_command": "Execute a shell command; expects a command string as parameter",
    "echo": "Print and return a message. This function echoes the input message."
}

# Function to store function metadata in ChromaDB
def store_function_metadata():
    for func, description in functions.items():
        collection.add(
            ids=[func],
            embeddings=[embedder.encode(description).tolist()],
            metadatas=[{"function": func}]
        )
    print("Function metadata stored successfully.")

# Uncomment the following line and run this file once to store metadata:
# store_function_metadata()

# Session memory to store past user queries (for context)
session_history = []

def retrieve_function(user_query):
    global session_history
    query_clean = user_query.strip().lower()

    # 1. Check if the query exactly matches a known custom function name
    # (You can add more if needed.)
    if query_clean == "hello_world":
        return "hello_world"

    # 2. Check custom_functions for an exact match (case-insensitive)
    for key in custom_functions.keys():
        if key.lower() == query_clean:
            return key

    # 3. Also check if the query exactly matches a default function
    for key in functions.keys():
        if key.lower() == query_clean:
            return key

    # 4. Fallback: Append the query to session history and perform vector search
    session_history.append(user_query)
    context_query = " ".join(session_history)
    query_embedding = embedder.encode(context_query).tolist()

    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    if results.get('ids') and results['ids'][0]:
        return results['metadatas'][0][0]['function']
    return None

