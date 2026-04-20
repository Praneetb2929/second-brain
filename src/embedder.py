import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Explicitly load .env from project root
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def get_embedding_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # This will tell us exactly what's happening
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found! Check your .env file.")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    return embeddings

def embed_texts(texts):
    model = get_embedding_model()
    vectors = model.embed_documents(texts)
    return vectors