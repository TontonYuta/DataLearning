"""
PROJECT 7: MACHINE LEARNING CUSTOMER CHURN PREDICTION PIPELINE
Data Mastery All-In-One (2026 Edition)
Trains an end-to-end Scikit-Learn Pipeline with Preprocessing,
Evaluates on Imbalanced Data, and Exports the Artifact for Production Serving.
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "customer_churn_features.csv"
MODEL_DIR = Path(__file__).resolve().parent
MODEL_SAVE_PATH = MODEL_DIR / "churn_model.joblib"
MLOPS_MODEL_PATH = BASE_DIR / "code" / "ch12_mlops" / "churn_model.joblib"

def train():
    print("=" * 65)
    print("PROJECT 7: CUSTOMER CHURN ML TRAINING PIPELINE")
    print("=" * 65)
    
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found!")
        return

    df = pd.read_csv(DATA_PATH)
    print(f"Dataset Loaded: {len(df):,} records with columns:")
    print(list(df.columns))
    
    target_col = "is_churn"
    feature_cols = [c for c in df.columns if c not in ["customer_id", target_col]]
    
    num_cols = ["tenure_months", "monthly_charges", "total_transactions", "days_since_last_login"]
    cat_cols = ["contract_type", "payment_method", "gender"]
    
    X = df[feature_cols]
    y = df[target_col]
    
    churn_rate = y.mean() * 100
    print(f"Baseline Churn Rate: {churn_rate:.2f}% ({y.sum():,} / {len(y):,})")
    
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
        import joblib
    except ImportError:
        print("[WARNING] scikit-learn or joblib not installed in current interpreter.")
        print("Please activate data_env: source data_env/bin/activate")
        return

    # 1. Train / Test Split (Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train Set: {len(X_train):,} samples | Test Set: {len(X_test):,} samples")

    # 2. Build Preprocessor Pipeline (No Data Leakage!)
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ]
    )

    # 3. Model Pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=100,
                max_depth=6,
                class_weight="balanced",
                random_state=42
            )),
        ]
    )

    # 4. Train
    print("\nTraining Random Forest Pipeline with Class Weighting...")
    pipeline.fit(X_train, y_train)

    # 5. Evaluate on Test Set
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    auc_score = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    
    print("\n" + "-" * 50)
    print("MODEL EVALUATION ON TEST SET (20% HOLDOUT)")
    print("-" * 50)
    print(f"ROC-AUC Score: {auc_score:.4f}")
    print("\nConfusion Matrix:")
    print(f"   TN: {cm[0,0]:<5} | FP: {cm[0,1]:<5}")
    print(f"   FN: {cm[1,0]:<5} | TP: {cm[1,1]:<5}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Retained (0)", "Churned (1)"]))

    # 6. Save Model Artifact
    joblib.dump(pipeline, MODEL_SAVE_PATH)
    print(f"[SUCCESS] Model artifact exported to: {MODEL_SAVE_PATH}")
    
    # Also copy to ch12_mlops for API serving
    MLOPS_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MLOPS_MODEL_PATH)
    print(f"[SUCCESS] Model artifact mirrored to: {MLOPS_MODEL_PATH}")
    print("=" * 65)

if __name__ == "__main__":
    train()
