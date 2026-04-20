# 🧠 Second Brain — Local AI Knowledge Assistant

A fully offline personal knowledge assistant built with RAG (Retrieval Augmented Generation). Drop in your PDFs and notes, ask questions in plain English, and get cited answers — all running locally with zero data leakage.

---

## Demo

> **Q: What is a Neural Network?**
> 
> A: A Neural Network is a computing system inspired by biological neural networks in animal brains. [Neural Networks and Deep Learning.txt]
> 
> Sources: Neural Networks and Deep Learning.txt

> **Q: What is the capital of France?**
> 
> I couldn't find this in your documents.

The second response is intentional — the app **refuses to hallucinate** and only answers from your documents.

---

## How It Works

```
Your PDFs/Notes → Chunker → Embedder → ChromaDB
                                            ↓
Your Question → Embedder → Similarity Search → Top-K Chunks → LLM → Cited Answer
```

1. **Ingestion** — Documents are loaded, split into overlapping chunks, embedded into vectors, and stored in ChromaDB locally
2. **Retrieval** — Your question is embedded and compared against stored vectors to find the most relevant chunks
3. **Generation** — Retrieved chunks + your question are sent to Llama 3.1 (via Groq) with a prompt that enforces citations and prevents hallucination

This pattern is called **RAG (Retrieval Augmented Generation)** — the most widely used pattern in enterprise AI today.

---

## Tech Stack

| Component | Tool | Purpose |
|---|---|---|
| LLM | Llama 3.1 via Groq | Answer generation |
| Embeddings | Gemini Embedding 001 | Text → vectors |
| Vector DB | ChromaDB | Local similarity search |
| Framework | LangChain | RAG pipeline orchestration |
| UI | Streamlit | Web interface |
| PDF parsing | PyMuPDF | Document loading |

**Cost: $0** — Groq free tier + Google AI Studio free tier. No credit card required.

---

## Project Structure

```
second-brain/
├── docs/                    ← Drop your PDFs and notes here
├── src/
│   ├── __init__.py
│   ├── document_loader.py   ← Reads PDFs and text files
│   ├── chunker.py           ← Splits text into overlapping chunks
│   ├── embedder.py          ← Converts text to vectors via Gemini
│   ├── vector_store.py      ← Saves/loads ChromaDB
│   ├── ingest.py            ← Runs the full ingestion pipeline
│   ├── retriever.py         ← Semantic similarity search
│   ├── rag_chain.py         ← LLM + context chain
│   └── prompts.py           ← Citation-enforcing system prompt
├── app.py                   ← Streamlit UI
├── .env                     ← API keys (never commit this)
├── .gitignore
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A free [Google AI Studio](https://aistudio.google.com) account (for embeddings)
- A free [Groq](https://console.groq.com) account (for LLM)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/second-brain.git
cd second-brain
```

**2. Create a virtual environment**
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up API keys**

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Get your keys:
- Google API key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Groq API key: [console.groq.com](https://console.groq.com) → API Keys → Create API key

### Usage

**1. Add your documents**

Drop any PDFs, `.txt`, or `.md` files into the `docs/` folder.

**2. Ingest documents**
```bash
python -m src.ingest
```

You should see:
```
Step 1: Loading documents...
Loaded X documents
Step 2: Chunking documents...
Created X chunks
Step 3: Embedding and saving to ChromaDB...
Saved X chunks to ChromaDB
Done! Your knowledge base is ready.
```

**3. Launch the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start asking questions.

> Re-run `python -m src.ingest` whenever you add new documents.

---

## Key Design Decisions

**Why overlapping chunks?**
Chunks overlap by 50 characters so that information at chunk boundaries is never lost. A fact split across two chunks still gets retrieved correctly.

**Why does it refuse to answer some questions?**
The system prompt explicitly instructs the LLM to only use the provided context and say "I couldn't find this in your documents" if the answer isn't there. This prevents hallucination — a critical property for a knowledge retrieval tool.

**Why Groq instead of OpenAI?**
Groq runs Llama 3.1 on custom hardware called LPUs (Language Processing Units), making it significantly faster than OpenAI for inference — and it's free.

**Why local ChromaDB instead of a cloud vector database?**
Privacy. Your documents never leave your machine. ChromaDB persists to disk so your knowledge base survives restarts without re-ingesting.

---

## Requirements

```
langchain
langchain-community
langchain-google-genai
langchain-groq
chromadb
streamlit
pymupdf
python-dotenv
google-generativeai
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## What I Learned

- How to build a production RAG pipeline from scratch — chunking, embedding, retrieval, and generation
- Why chunk overlap matters for retrieval quality
- How to enforce citation behavior in LLM prompts to prevent hallucination
- How vector similarity search works — same embedding model must be used for both ingestion and query
- Debugging real API issues — rate limits, deprecated model names, key management, import paths

---

## Future Improvements

- [ ] Auto-tagging — LLM generates topic tags when a file is uploaded
- [ ] Weekly digest — summarizes everything added that week
- [ ] Contradiction detector — finds conflicting information across documents
- [ ] Hybrid retrieval — combine BM25 keyword search with vector search for better precision
- [ ] Evaluation pipeline — measure retrieval quality with Ragas metrics

---

## License

MIT
