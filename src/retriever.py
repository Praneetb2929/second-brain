import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
except:
    pass

def get_api_key(key_name):
    try:
        import streamlit as st
        return st.secrets[key_name]
    except:
        return os.getenv(key_name)

def get_embedding_model():
    api_key = get_api_key("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found!")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    return embeddings

def embed_texts(texts):
    model = get_embedding_model()
    vectors = model.embed_documents(texts)
    return vectors
