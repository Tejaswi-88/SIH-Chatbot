# app/controllers/chat_controller.py

from app.services.translation_service import translate_text
from app.services.llm_service import generate_response
from app.services.knowledge_service import retrieve

# -----------------------------------------------------------
# ✅ Supported Languages
# -----------------------------------------------------------
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "bn": "Bengali",
    "ta": "Tamil"
}


# -----------------------------------------------------------
# ✅ Main Chat Handling Function (with RAG)
# -----------------------------------------------------------
async def handle_user_message(user_message: str, language: str):
    """
    Main function to process user messages:
    1. Detects user language
    2. Translates to English (if needed)
    3. Retrieves relevant context from knowledge base
    4. Generates AI response (LLM)
    5. Translates back to user language
    """

    # 1️⃣ Validate Language
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language code: {language}")

    print(f"🌍 Received message: '{user_message}' in {SUPPORTED_LANGUAGES[language]}")

    # 2️⃣ Translate to English (if not already English)
    if language != "en":
        translated_input = await translate_text(user_message, src_lang=language, dest_lang="en")
        print(f"🔁 Translated to English: {translated_input}")
    else:
        translated_input = user_message

    # 3️⃣ Retrieve relevant knowledge chunks
    context_chunks = retrieve(translated_input, top_k=5)
    context_text = "\n".join([c[0] for c in context_chunks])
    final_prompt = f"Context: {context_text}\nQuestion: {translated_input}"
    print(f"📚 Contextual Prompt Sent to LLM:\n{final_prompt}")

    # 4️⃣ Generate Response using AI Model
    ai_response_en = await generate_response(final_prompt)
    print(f"🤖 AI Response (English): {ai_response_en}")

    # 5️⃣ Translate Response back to user language
    if language != "en":
        final_response = await translate_text(ai_response_en, src_lang="en", dest_lang=language)
        print(f"🌐 Translated Response: {final_response}")
    else:
        final_response = ai_response_en

    return final_response


    # 3️⃣ Generate Response using AI Model
    #ai_response_en = await generate_response(translated_input)
    #print(f"🤖 AI Response (English): {ai_response_en}")

    # 4️⃣ Translate Response back to user language
    #if language != "en":
    #    final_response = await translate_text(ai_response_en, src_lang="en", dest_lang=language)
    #    print(f"🌐 Translated Response: {final_response}")
    #else:
    #    final_response = ai_response_en
#
#    return final_response 
