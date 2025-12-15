# app/routes/admin_routes.py

from fastapi import APIRouter, UploadFile, File
from app.services.knowledge_service import ingest_documents
import os

router = APIRouter()

UPLOAD_FOLDER = "college_data"

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        saved_files.append(file_location)

    # Trigger ingestion for FAISS / RAG
    ingest_documents(UPLOAD_FOLDER)

    return {"message": f"{len(saved_files)} files uploaded and ingested successfully!"}
