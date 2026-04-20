from src.vector_store import load_vector_store

def retrieve(query, k=4):
    """
    query: the user's question as a string
    k: how many chunks to retrieve (4 is a good balance)
    """
    # Load the existing vector store from disk
    vector_store = load_vector_store()

    # similarity_search embeds the query and finds
    # the k most similar chunks in ChromaDB
    results = vector_store.similarity_search(query, k=k)

    # Each result has .page_content (the text) and .metadata (source filename)
    chunks = []
    for result in results:
        chunks.append({
            "text": result.page_content,
            "source": result.metadata.get("source", "unknown")
        })

    return chunks