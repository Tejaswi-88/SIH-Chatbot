# app/services/knowledge_service.py

import os
import json
import faiss
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import PyPDF2
import docx

from app.services.vector_service import add_to_faiss  # your FAISS ingestion function
import shutil
# -------------------------------
# Model for embeddings
# -------------------------------
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# -------------------------------
# FAISS index setup
# -------------------------------
INDEX_FILE = "faiss_index.index"
METADATA_FILE = "faiss_metadata.json"

# Allowed file types per category
FILE_CATEGORIES = {
    "circulars": [".pdf", ".docx", ".doc"],
    "faq": [".json"],
    "messages": [".txt"],
    "excel": [".xlsx", ".xls"]
}

BASE_FOLDER = "college_data"

if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
else:
    index = faiss.IndexFlatL2(384)  # dimension of MiniLM embeddings
    metadata = []

# -------------------------------
# Helper functions to read files
# -------------------------------
def read_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext == ".docx":
        return read_docx(file_path)
    elif ext == ".txt":
        return read_txt(file_path)
    else:
        return ""  # skip unsupported


# -------------------------------
# Ingest documents and build embeddings
# -------------------------------
def ingest_documents(upload_folder: str = BASE_FOLDER):
    """
    Processes files in upload_folder:
    1. Sorts files into subfolders based on type
    2. Updates FAISS embeddings for RAG
    """
    print("📥 Starting document ingestion...")

    # 1️⃣ Ensure subfolders exist
    for category in FILE_CATEGORIES:
        folder_path = os.path.join(BASE_FOLDER, category)
        os.makedirs(folder_path, exist_ok=True)

    # 2️⃣ Sort files into correct subfolders
    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_name)[1].lower()
            moved = False
            for category, extensions in FILE_CATEGORIES.items():
                if ext in extensions:
                    dest_path = os.path.join(BASE_FOLDER, category, file_name)
                    shutil.move(file_path, dest_path)
                    moved = True
                    print(f"➡️ Moved {file_name} → {category}/")
                    break
            if not moved:
                print(f"⚠️ Unsupported file type: {file_name}, skipping.")

    # 3️⃣ Ingest all documents in subfolders into FAISS
    for category, extensions in FILE_CATEGORIES.items():
        folder_path = os.path.join(BASE_FOLDER, category)
        for root, _, files in os.walk(folder_path):
            for f in files:
                if os.path.splitext(f)[1].lower() in extensions:
                    file_path = os.path.join(root, f)
                    add_to_faiss(file_path)
                    print(f"✅ Ingested: {file_path}")

    print("📌 Document ingestion completed!")

    
# -------------------------------
# Split text into manageable chunks
# -------------------------------
def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# -------------------------------
# Search for relevant chunks
# -------------------------------
def retrieve(query: str, top_k: int = 5) -> List[Tuple[str, float]]:
    query_emb = embedding_model.encode([query])
    D, I = index.search(np.array(query_emb, dtype=np.float32), top_k)
    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(metadata):
            results.append((metadata[idx]["text"], float(score)))
    return results
