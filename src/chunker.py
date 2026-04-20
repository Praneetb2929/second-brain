def chunk_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    chunk_size: how many characters per chunk
    chunk_overlap: how many characters the next chunk shares with the previous
    """
    all_chunks = []

    for doc in documents:
        text = doc["text"]
        source = doc["source"]

        # We slide a window across the text
        # Start at 0, move forward by (chunk_size - chunk_overlap) each time
        start = 0
        while start < len(text):
            end = start + chunk_size

            # slice the text from start to end
            chunk_text = text[start:end]

            # skip empty chunks (can happen at the end of a doc)
            if chunk_text.strip():
                all_chunks.append({
                    "text": chunk_text,
                    "source": source  # keep track of which file this came from
                })

            # move the window forward, but back up by overlap amount
            start += chunk_size - chunk_overlap

    print(f"Created {len(all_chunks)} chunks")
    return all_chunks