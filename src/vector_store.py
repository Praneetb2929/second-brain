import os
import chromadb
from src.embedder import get_embedding_model
from langchain_community.vectorstores import Chroma

# This is the folder where ChromaDB saves its data on disk
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

def save_to_vector_store(chunks):
    """
    Takes a list of chunk dicts, embeds them, saves to ChromaDB.
    """
    # Separate the text and metadata for storage
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"]} for chunk in chunks]

    # get_embedding_model() returns the Gemini embedder
    embedding_model = get_embedding_model()

    # Chroma.from_texts does 3 things:
    # 1. Embeds all texts using the embedding model
    # 2. Stores the embeddings in ChromaDB
    # 3. Attaches metadata (source filename) to each entry
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=CHROMA_PATH  # saves to disk so it survives restarts
    )

    print(f"Saved {len(texts)} chunks to ChromaDB")
    return vector_store

def load_vector_store():
    """
    Loads an existing ChromaDB from disk.
    Call this when the app starts — avoids re-ingesting every time.
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )
    return vector_store