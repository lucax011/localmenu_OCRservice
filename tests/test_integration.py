import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_ocr_extract():
    with open("tests/assets/menu1.jpg", "rb") as f:
        resp = client.post("/ocr/extract", files={"file": ("menu1.jpg", f, "image/jpeg")})
    assert resp.status_code == 200
    assert "items" in resp.json()
