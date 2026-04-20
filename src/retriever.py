import os
from src.vector_store import load_vector_store

def retrieve(query, k=4):
    # Check if chroma_db exists yet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chroma_path = os.path.join(base_dir, "chroma_db")

    if not os.path.exists(chroma_path):
        return []

    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)

    chunks = []
    for result in results:
        chunks.append({
            "text": result.page_content,
            "source": result.metadata.get("source", "unknown")
        })

    return chunks
