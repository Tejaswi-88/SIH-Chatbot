# app/services/vector_service.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from typing import Union

# -----------------------------
# FAISS & Embedding Setup
# -----------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight, multilingual
VECTOR_STORE_PATH = "faiss_index.index"
DOC_METADATA_PATH = "doc_metadata.pkl"

# Load or create FAISS index
if os.path.exists(VECTOR_STORE_PATH):
    index = faiss.read_index(VECTOR_STORE_PATH)
    with open(DOC_METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)  # 384 for MiniLM embeddings
    metadata = {}

# Load embedding model
model = SentenceTransformer(EMBEDDING_MODEL)


# -----------------------------
# Helper: Extract text from file
# -----------------------------
def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages])

    elif ext in [".docx", ".doc"]:
        from docx import Document
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".json":
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data)

    elif ext in [".xlsx", ".xls"]:
        import pandas as pd
        df = pd.read_excel(file_path)
        return df.to_csv(index=False)

    else:
        return ""  # unsupported


# -----------------------------
# Add a document to FAISS
# -----------------------------
def add_to_faiss(file_path: str):
    text = extract_text(file_path)
    if not text.strip():
        print(f"⚠️ No text extracted from {file_path}, skipping.")
        return

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    # Create embeddings and add to FAISS
    embeddings = model.encode(chunks)
    index.add(embeddings)

    # Save metadata
    for i, chunk in enumerate(chunks):
        metadata[len(metadata)] = {"text": chunk, "source": file_path}

    # Save FAISS index & metadata
    faiss.write_index(index, VECTOR_STORE_PATH)
    with open(DOC_METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"✅ Added {file_path} to FAISS with {len(chunks)} chunks.")


# -----------------------------
# Retrieve top-K similar chunks
# -----------------------------
def retrieve(query: str, top_k: int = 5):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, top_k)
    results = []
    for i in I[0]:
        if i in metadata:
            results.append((metadata[i]["text"], metadata[i]["source"]))
    return results
