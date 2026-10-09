import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def detect_scam(transcript: str) -> dict:
    prompt = f"""
    Analyze this real-time transcript for phone scams targeting the elderly.
    Transcript: "{transcript}"
    
    Return strict JSON: {{"is_threat": bool, "reasoning": "str", "warning_text": "str"}}
    """
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)
