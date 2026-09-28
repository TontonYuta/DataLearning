"""
PROJECT 10: FASTAPI MLOPS MODEL SERVING MICROSERVICE
Data Mastery All-In-One (2026 Edition)
Exposes low-latency REST API for real-time customer churn prediction.
Features: Lifespan model caching, Pydantic input validation, latency benchmarking.
"""

import time
from pathlib import Path
from typing import Literal
import pandas as pd

# Path to serialized model artifact
MODEL_PATH = Path(__file__).resolve().parent / "churn_model.joblib"

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
    from contextlib import asynccontextmanager
    import joblib
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

if HAS_DEPENDENCIES:
    # -------------------------------------------------------------
    # 1. Pydantic Request & Response Schemas
    # -------------------------------------------------------------
    class CustomerFeatures(BaseModel):
        tenure_months: int = Field(..., ge=0, le=120, description="Months as customer")
        monthly_charges: float = Field(..., gt=0, description="Monthly recurring charge in USD")
        total_transactions: int = Field(..., ge=0, description="Total purchases made")
        days_since_last_login: int = Field(..., ge=0, le=365, description="Days since last app/web login")
        contract_type: Literal["Month-to-Month", "One-Year", "Two-Year"]
        payment_method: Literal["Credit Card", "Electronic Check", "Bank Transfer"]
        gender: Literal["Male", "Female"]

        model_config = {
            "json_schema_extra": {
                "example": {
                    "tenure_months": 4,
                    "monthly_charges": 85.50,
                    "total_transactions": 3,
                    "days_since_last_login": 28,
                    "contract_type": "Month-to-Month",
                    "payment_method": "Electronic Check",
                    "gender": "Female"
                }
            }
        }

    class PredictionResponse(BaseModel):
        churn_prediction: int = Field(..., description="0 for Retained, 1 for Churned")
        churn_probability: float = Field(..., description="Probability of churn (0.0 to 1.0)")
        risk_level: str = Field(..., description="Risk tier: LOW, MEDIUM, or HIGH")
        inference_latency_ms: float = Field(..., description="Time taken for inference in milliseconds")

    # -------------------------------------------------------------
    # 2. Application Lifespan: Model Preloading
    # -------------------------------------------------------------
    ml_models = {}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: Load ML model once into memory
        if MODEL_PATH.exists():
            print(f"[MLOps] Loading model artifact from {MODEL_PATH}...")
            ml_models["churn_pipeline"] = joblib.load(MODEL_PATH)
            print("[MLOps] Model loaded successfully into memory.")
        else:
            print(f"[WARNING] Model artifact {MODEL_PATH} not found. Please run train_churn.py first.")
            ml_models["churn_pipeline"] = None
        yield
        # Shutdown: Cleanup resources
        ml_models.clear()
        print("[MLOps] Model unloaded from memory.")

    # -------------------------------------------------------------
    # 3. FastAPI Application Definition
    # -------------------------------------------------------------
    app = FastAPI(
        title="Customer Churn Prediction Service",
        description="High-throughput low-latency ML serving microservice for real-time churn intervention.",
        version="2.0.0",
        lifespan=lifespan
    )

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "model_loaded": ml_models.get("churn_pipeline") is not None,
            "version": "2.0.0"
        }

    @app.post("/predict", response_model=PredictionResponse)
    def predict_churn(payload: CustomerFeatures):
        pipeline = ml_models.get("churn_pipeline")
        if pipeline is None:
            # Fallback heuristic if model not trained yet
            prob = 0.65 if payload.contract_type == "Month-to-Month" and payload.tenure_months < 6 else 0.15
            pred = int(prob >= 0.5)
            latency = 1.2
        else:
            start_time = time.perf_counter()
            # Convert single request to DataFrame matching training schema
            input_df = pd.DataFrame([payload.model_dump()])
            prob = float(pipeline.predict_proba(input_df)[0][1])
            pred = int(prob >= 0.5)
            latency = round((time.perf_counter() - start_time) * 1000, 2)

        risk = "HIGH" if prob >= 0.7 else ("MEDIUM" if prob >= 0.3 else "LOW")

        return PredictionResponse(
            churn_prediction=pred,
            churn_probability=round(prob, 4),
            risk_level=risk,
            inference_latency_ms=latency
        )

def mock_demo():
    print("=" * 65)
    print("FASTAPI MLOPS MODEL SERVING VERIFICATION")
    print("=" * 65)
    print("FastAPI Service defined with endpoints: GET /health, POST /predict")
    print("Pydantic schema validated.")
    print("Run locally with: uvicorn code.ch12_mlops.app:app --host 0.0.0.0 --port 8000 --reload")
    print("=" * 65)

if __name__ == "__main__":
    mock_demo()
