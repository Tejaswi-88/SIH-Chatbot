# app/middleware/language_middleware.py

from fastapi import Request
from langdetect import detect, DetectorFactory
from typing import Tuple

# Ensures consistent language detection
DetectorFactory.seed = 0

# Supported languages for your chatbot
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "bn": "Bengali",
    "ta": "Tamil"
}

# Optional: add Romanized variants mapping if you want
ROMANIZED_MAPPING = {
    "hi": ["hindi", "hindi-roman", "roman-hindi"],
    "te": ["telugu", "telugu-roman", "roman-telugu"],
    "bn": ["bengali", "bengali-roman", "bengali-telugu"],
    "ta": ["tamil", "tamil-roman", "tamil-telugu"]
}


# -----------------------------------------------------------
# Detect language from user text
# -----------------------------------------------------------
def detect_language(text: str) -> str:
    """
    Detects language of the input text and normalizes to supported language codes.
    Defaults to English if detection fails or unsupported.
    """
    try:
        detected = detect(text).lower()  # returns ISO 639-1 code
    except:
        detected = "en"

    if detected in SUPPORTED_LANGUAGES:
        return detected
    else:
        return "en"  # fallback


# -----------------------------------------------------------
# Optional: handle transliteration
# -----------------------------------------------------------
def normalize_text(text: str, lang_code: str) -> str:
    """
    Converts Romanized input to proper script if needed.
    Currently placeholder: you can integrate IndicTrans / Aksharamukha here.
    """
    # Example: placeholder for Roman Hindi -> Hindi script
    if lang_code in ROMANIZED_MAPPING:
        # Implement transliteration if needed
        # For now, just return text unchanged
        return text

    return text


# -----------------------------------------------------------
# Middleware for FastAPI
# -----------------------------------------------------------
async def language_middleware(request: Request, call_next):
    """
    FastAPI middleware to detect and normalize language for incoming requests.
    Attaches 'lang_code' and 'normalized_text' to request.state for controllers.
    """
    try:
        body = await request.json()
        text = body.get("message") or ""
    except:
        text = ""

    lang_code = detect_language(text)
    normalized_text = normalize_text(text, lang_code)

    # Attach to request.state for downstream usage
    request.state.lang_code = lang_code
    request.state.normalized_text = normalized_text

    response = await call_next(request)
    return response
