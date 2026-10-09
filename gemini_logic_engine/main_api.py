from fastapi import FastAPI
from pydantic import BaseModel
from scam_defense import detect_scam
from environment_tuner import get_dsp_params
from interspecies_bridge import map_command_to_haptic

app = FastAPI(title="OmniHear-AI Backend Engine")

class TranscriptInput(BaseModel):
    text: str
    environment: str

class PetCommandInput(BaseModel):
    command: str

@app.post("/analyze-transcript")
async def analyze_transcript(payload: TranscriptInput):
    threat_status = detect_scam(payload.text)
    dsp_params = get_dsp_params(payload.text, payload.environment)
    return {"scam_alert": threat_status, "dsp_tuning": dsp_params}

@app.post("/pet-command")
async def pet_command(payload: PetCommandInput):
    haptic_pattern = map_command_to_haptic(payload.command)
    return {"haptic_pattern": haptic_pattern}
