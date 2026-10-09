import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def map_command_to_haptic(command: str) -> dict:
    prompt = f"""
    Map the human intent of this pet command to a distinct collar vibration pattern for a deaf dog.
    Command: "{command}"
    
    Return strict JSON: {{"intent": "str", "vibration_pulses": int, "pulse_duration_ms": int, "intensity": int 0-255}}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)
