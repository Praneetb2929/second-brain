import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.prompts import RAG_PROMPT
from src.retriever import retrieve

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

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

    # Using Groq with Llama3 — free and fast
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

    response = llm.invoke(filled_prompt)
    answer = response.content
    sources = list(set([chunk["source"] for chunk in chunks]))

    return answer, sources