import whisper
import pyaudio
import numpy as np
import requests

MODEL = whisper.load_model("tiny.en")
API_URL = "http://localhost:8000/analyze-transcript"

def stream_audio_to_text():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16000)
    
    print("Listening for elderly user transcript...")
    while True:
        data = stream.read(16000)
        audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        
        result = MODEL.transcribe(audio_np, fp16=False)
        text = result["text"].strip()
        
        if text:
            print(f"Captured: {text}")
            res = requests.post(API_URL, json={"text": text, "environment": "Phone Call"})
            if res.status_code == 200:
                data = res.json()
                if data["scam_alert"]["is_threat"]:
                    print(f"!!! SCAM WARNING: {data['scam_alert']['warning_text']} !!!")

if __name__ == "__main__":
    stream_audio_to_text()
