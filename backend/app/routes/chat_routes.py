# app/routes/chat_routes.py
from fastapi import APIRouter, HTTPException
from app.controllers.chat_controller import handle_user_message
from pydantic import BaseModel
from app.db.connection import db

# -----------------------------------------------------------
# ✅ Initialize Router
# -----------------------------------------------------------
router = APIRouter(tags=["Chatbot"])

# -----------------------------------------------------------
# ✅ Request Schema
# -----------------------------------------------------------
class ChatRequest(BaseModel):
    user_message: str
    language: str  # e.g., "en", "hi", "te", "bn", "ta"


# -----------------------------------------------------------
# ✅ POST Endpoint — Handles Chat Messages
# -----------------------------------------------------------
@router.post("/")
async def chat_endpoint(request: ChatRequest):
    """
    Handles chat messages from frontend, detects language, 
    translates, processes through model, and returns multilingual response.
    """
    try:
        response = await handle_user_message(request.user_message, request.language)
        return {"reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
