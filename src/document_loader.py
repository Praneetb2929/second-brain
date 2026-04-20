import os
import fitz

def load_documents(docs_folder=None):
    if docs_folder is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docs_folder = os.path.join(base_dir, "docs")

    documents = []

    for filename in os.listdir(docs_folder):
        filepath = os.path.join(docs_folder, filename)

        if filename.endswith(".pdf"):
            pdf = fitz.open(filepath)
            full_text = ""
            for page in pdf:
                full_text += page.get_text()
            pdf.close()
            documents.append({
                "text": full_text,
                "source": filename
            })

        elif filename.endswith(".txt") or filename.endswith(".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                full_text = f.read()
            documents.append({
                "text": full_text,
                "source": filename
            })

    print(f"Loaded {len(documents)} documents")
    return documents