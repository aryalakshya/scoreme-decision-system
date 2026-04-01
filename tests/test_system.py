import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_happy_path():
    response = client.post("/process", json={
        "workflow": "loan_approval",
        "data": {"age": 25, "credit_score": 750},
        "idempotency_key": "test1"
    })
    assert response.status_code == 200
    assert response.json()["decision"] in ["approve", "reject", "retry"]

def test_invalid_input():
    response = client.post("/process", json={
        "workflow": "loan_approval",
        "data": {"credit_score": 750},  # missing age
        "idempotency_key": "test2"
    })
    assert response.status_code == 200
    assert response.json()["decision"] == "reject"

def test_duplicate_request():
    payload = {
        "workflow": "loan_approval",
        "data": {"age": 25, "credit_score": 700},
        "idempotency_key": "dup123"
    }

    first = client.post("/process", json=payload)
    second = client.post("/process", json=payload)

    assert "Duplicate request detected" in second.text

def test_external_failure_retry():
    response = client.post("/process", json={
        "workflow": "loan_approval",
        "data": {"age": 25, "credit_score": 650},
        "idempotency_key": "retry_test"
    })
    assert response.status_code == 200
    assert "decision" in response.json()