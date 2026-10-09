import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_dsp_params(transcript: str, env_desc: str) -> dict:
    prompt = f"""
    Determine local DSP hardware adjustments based on this acoustic environment.
    Acoustic context: {env_desc}
    Transcript context: {transcript}
    
    Return strict JSON: {{"noise_cancellation_level": int 0-10, "speech_boost": int 0-10, "mic_focus": "Omni"|"Front"}}
    """
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)
