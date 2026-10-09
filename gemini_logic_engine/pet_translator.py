import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_pet_vocalization(audio_file_path: str) -> dict:
    """Uses Gemini to classify pet audio (requires uploading file via File API)."""
    # Assuming audio_file_path points to a locally saved .wav of a bark/whine
    audio_file = client.files.upload(file=audio_file_path)
    
    prompt = """
    Listen to this dog vocalization. Classify the likely intent or emotional state.
    Categories: Alert/Alarm, Playful, Anxious/Stressed, Pain, Greeting.
    Return strict JSON: {"classification": "str", "confidence": int, "owner_alert_message": "str"}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[audio_file, prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    
    # Cleanup
    client.files.delete(name=audio_file.name)
    return json.loads(response.text)
