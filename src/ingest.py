from src.document_loader import load_documents
from src.chunker import chunk_documents
from src.vector_store import save_to_vector_store

def ingest():
    print("Step 1: Loading documents...")
    documents = load_documents()

    if not documents:
        print("No documents found in docs/ folder. Add some PDFs or text files.")
        return

    print("Step 2: Chunking documents...")
    chunks = chunk_documents(documents)

    print("Step 3: Embedding and saving to ChromaDB...")
    save_to_vector_store(chunks)

    print("Done! Your knowledge base is ready.")

# This runs when you execute: python src/ingest.py
if __name__ == "__main__":
    ingest()