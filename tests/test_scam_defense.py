import pytest
from fastapi.testclient import TestClient
from gemini_logic_engine.main_api import app

client = TestClient(app)

def test_safe_conversation():
    payload = {
        "text": "Hi grandma, it's me. Can you pass the potatoes?",
        "environment": "Dinner table"
    }
    # Mocking the Gemini call is recommended in CI, but assuming live test here
    response = client.post("/analyze-transcript", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scam_alert"]["is_threat"] is False

def test_scam_conversation():
    payload = {
        "text": "This is the IRS. You owe back taxes and will be arrested unless you pay in target gift cards.",
        "environment": "Phone Call"
    }
    response = client.post("/analyze-transcript", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["scam_alert"]["is_threat"] is True
