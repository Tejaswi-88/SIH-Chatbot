# app/services/llm_service.py

import os
import requests
import asyncio

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "google/flan-t5-small")  # default lightweight model
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


# -----------------------------------------------------------
# ✅ Generate AI Response
# -----------------------------------------------------------
async def generate_response(prompt: str) -> str:
    """
    Sends prompt to Hugging Face Inference API and returns model response.
    """
    try:
        response = await asyncio.to_thread(_call_hf_api, prompt)
        return response.strip()
    except Exception as e:
        print(f"❌ Hugging Face API error: {e}")
        return "I'm having trouble responding right now. Please try again later."


# -----------------------------------------------------------
# 🔹 Private helper function (sync call wrapped in async)
# -----------------------------------------------------------
def _call_hf_api(prompt: str) -> str:
    """
    Makes a synchronous HTTP request to HF API (called inside async wrapper)
    """
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}  # ensures the model is loaded if cold
    }

    response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=60)

    if response.status_code != 200:
        raise Exception(f"HF API failed ({response.status_code}): {response.text}")

    data = response.json()

    # HF Inference API returns a list of dicts with 'generated_text'
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    # fallback
    return str(data)
