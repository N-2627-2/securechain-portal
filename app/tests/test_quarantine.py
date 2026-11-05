import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_quarantine_success():
    payload = {
        "alert_id": "3f6c1c2e-8a4b-4f0e-9a52-1b7d2c9e0a11",
        "node_id": "sensor-wh1-0042",
        "site_id": "warehouse-1",
        "reason": "Unauthorized Modbus write",
        "severity": "low",
        "expires_in_minutes": 60
    }
    response = client.post("/api/v1/quarantine", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data["node_id"] == "sensor-wh1-0042"
    assert data["status"] == "active"

def test_quarantine_missing_approval_high_severity():
    payload = {
        "alert_id": "3f6c1c2e-8a4b-4f0e-9a52-1b7d2c9e0a11",
        "node_id": "sensor-wh1-0042",
        "site_id": "warehouse-1",
        "reason": "Unauthorized Modbus write",
        "severity": "high",
        "expires_in_minutes": 60
    }
    response = client.post("/api/v1/quarantine", json=payload)
    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "APPROVAL_REQUIRED"