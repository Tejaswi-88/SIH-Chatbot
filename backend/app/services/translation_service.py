# app/services/translation_service.py

from deep_translator import GoogleTranslator

# -----------------------------------------------------------
# ✅ Translation Utility using GoogleTranslator
# -----------------------------------------------------------
async def translate_text(text: str, src_lang: str, dest_lang: str) -> str:
    """
    Translates text from src_lang to dest_lang using Google Translator.
    Supported languages: English, Hindi, Telugu, Bengali, Tamil
    """
    try:
        if src_lang == dest_lang:
            return text  # No translation needed

        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
        return translated

    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return text  # Fallback to original text if translation fails
