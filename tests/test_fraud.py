from fastapi.testclient import TestClient
from fraudrt.main import app
from fraudrt import serve
client = TestClient(app)

def setup_function():
    serve.CACHE.clear(); serve.EVENTS.clear()

def test_flags_risky_and_caches():
    risky = {"amount": 1000, "foreign": 1, "velocity": 8, "idempotency_key": "k1"}
    a = client.post("/score", json=risky).json()
    b = client.post("/score", json=risky).json()
    safe = client.post("/score", json={"amount": 12, "foreign": 0, "velocity": 1}).json()
    assert a["label"] == "fraud" and a["charged"] is False
    assert b["cached"] is True
    assert safe["label"] == "legitimate"
    assert client.post("/score", json={"amount": 1}).status_code == 422
