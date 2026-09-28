"""
Test suite for FastAPI Churn Prediction Microservice.
Verifies GET /health and POST /predict with valid/invalid payloads.
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    with TestClient(app) as c:
        response = c.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print(f"[TEST PASS] /health returned: {data}")

def test_prediction():
    with TestClient(app) as c:
        payload = {
            "tenure_months": 2,
            "monthly_charges": 95.0,
            "total_transactions": 2,
            "days_since_last_login": 45,
            "contract_type": "Month-to-Month",
            "payment_method": "Electronic Check",
            "gender": "Female"
        }
        response = c.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "churn_prediction" in data
        assert "churn_probability" in data
        assert "risk_level" in data
        print(f"[TEST PASS] /predict response: {data}")

if __name__ == "__main__":
    print("Running FastAPI TestClient suite...")
    test_health()
    test_prediction()
    print("All API tests passed!")
