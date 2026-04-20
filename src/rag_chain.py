import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.prompts import RAG_PROMPT
from src.retriever import retrieve

# Load .env for local development
try:
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
except:
    pass

def get_api_key(key_name):
    # Try Streamlit secrets first (cloud), then .env (local)
    try:
        import streamlit as st
        return st.secrets[key_name]
    except:
        return os.getenv(key_name)

def ask(question):
    chunks = retrieve(question, k=4)

    if not chunks:
        return "No relevant documents found.", []

    context_parts = []
    for chunk in chunks:
        context_parts.append(f"[{chunk['source']}]\n{chunk['text']}")

    context = "\n\n---\n\n".join(context_parts)

    filled_prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=get_api_key("GROQ_API_KEY"),
        temperature=0.2
    )

    response = llm.invoke(filled_prompt)
    answer = response.content
    sources = list(set([chunk["source"] for chunk in chunks]))

    return answer, sources
