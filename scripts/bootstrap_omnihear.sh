#!/bin/bash
set -e

echo "[1/4] Setting up OmniHear-AI Virtual Environment..."
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn google-genai openai-whisper pyaudio pydantic

echo "[2/4] Compiling Rust DSP Core for Human Earpiece..."
cd hardware/human_dsp_earpiece
cargo build --release
cd ../..

echo "[3/4] Readying ESP32 Animal Collar Firmware Build Pipeline..."
# Requires arduino-cli configured locally
# arduino-cli compile --fqbn esp32:esp32:esp32 hardware/animal_haptic_collar/esp32_haptic.ino

echo "[4/4] Launching Gemini Logic Engine Backend..."
cd gemini_logic_engine
uvicorn main_api:app --reload --port 8000 &
BACKEND_PID=$!

echo "OmniHear-AI environment running. Backend PID: $BACKEND_PID"
wait
