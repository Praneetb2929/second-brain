import streamlit as st
import os
import shutil
from src.ingest import ingest
from src.rag_chain import ask

# --- Page config ---
st.set_page_config(
    page_title="Second Brain",
    page_icon="🧠",
    layout="centered"
)

st.title("Your Local Second Brain")
st.caption("Upload your notes and PDFs, then ask anything about them.")

# --- File uploader section ---
st.subheader("Add documents")
uploaded_files = st.file_uploader(
    "Upload PDFs or text files",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

if uploaded_files:
    # Save uploaded files to the docs/ folder
    os.makedirs("docs", exist_ok=True)
    for file in uploaded_files:
        save_path = os.path.join("docs", file.name)
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

    st.success(f"Saved {len(uploaded_files)} file(s) to docs/")

    # Button to trigger ingestion
    if st.button("Index documents"):
        with st.spinner("Reading, chunking, and embedding your documents..."):
            ingest()
        st.success("Done! You can now ask questions.")

st.divider()

# --- Chat section ---
st.subheader("Ask your knowledge base")

# st.session_state persists data between interactions
# Without this, chat history disappears on every rerun
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show sources if this was an assistant message
        if message["role"] == "assistant" and "sources" in message:
            if message["sources"]:
                st.caption("Sources: " + ", ".join(message["sources"]))

# Chat input box at the bottom
if prompt := st.chat_input("Ask something about your documents..."):

    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get answer from RAG chain
    with st.chat_message("assistant"):
        with st.spinner("Searching your documents..."):
            answer, sources = ask(prompt)

        st.markdown(answer)

        if sources:
            st.caption("Sources: " + ", ".join(sources))

    # Save assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })