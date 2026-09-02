"""
FinGuard AI - ML Model Training Pipeline
Trains:
1. Intent Classification Model (TF-IDF + Logistic Regression)
2. Risk Assessment Model (Gradient Boosting Regressor)
3. Decision Prediction Model (Random Forest Classifier)
4. Liquidity Impact Forecaster
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error, r2_score, accuracy_score
from sklearn.pipeline import Pipeline

ML_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ML_DIR, "data")
MODELS_DIR = os.path.join(ML_DIR, "models")
EVAL_DIR = os.path.join(ML_DIR, "evaluation")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)

def train_intent_classifier():
    print("\n--- Training Financial Intent Classifier ---")
    data_path = os.path.join(DATA_DIR, "intent_dataset.csv")
    df = pd.read_csv(data_path)
    
    # Feature text combine agent and description
    df['text_feature'] = df['agent_name'] + " " + df['description']
    X = df['text_feature']
    y = df['intent_label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=1500)),
        ('clf', LogisticRegression(C=2.0, max_iter=500, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"Intent Classifier Test Accuracy: {acc * 100:.2f}%")
    report = classification_report(y_test, y_pred, output_dict=True)
    
    model_path = os.path.join(MODELS_DIR, "intent_classifier.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Saved Intent Model to {model_path}")
    
    return {"accuracy": acc, "report": report}

def train_risk_and_decision_models():
    print("\n--- Training Multi-Factor Risk & Decision Models ---")
    data_path = os.path.join(DATA_DIR, "risk_dataset.csv")
    df = pd.read_csv(data_path)
    
    feature_cols = [
        "amount",
        "available_cash",
        "required_reserve",
        "pending_concurrent_outflows",
        "agent_trust_score",
        "agent_confidence",
        "policy_violations",
        "urgency_score",
        "liquidity_ratio_before",
        "projected_liquidity_ratio",
        "global_projected_liquidity_ratio",
        "reserve_shortfall",
        "cross_agent_conflict_severity"
    ]
    
    X = df[feature_cols]
    y_risk = df["risk_score"]
    y_decision = df["recommended_decision"]
    
    X_train, X_test, y_risk_train, y_risk_test, y_dec_train, y_dec_test = train_test_split(
        X, y_risk, y_decision, test_size=0.2, random_state=42
    )
    
    # 1. Continuous Risk Score Model
    risk_model = GradientBoostingRegressor(
        n_estimators=120,
        learning_rate=0.08,
        max_depth=4,
        random_state=42
    )
    risk_model.fit(X_train, y_risk_train)
    risk_pred = risk_model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_risk_test, risk_pred))
    r2 = r2_score(y_risk_test, risk_pred)
    print(f"Risk Score Regressor RMSE: {rmse:.3f}, R2 Score: {r2:.3f}")
    
    risk_path = os.path.join(MODELS_DIR, "risk_scorer.joblib")
    joblib.dump(risk_model, risk_path)
    print(f"Saved Risk Scorer Model to {risk_path}")
    
    # 2. Decision Multi-Class Classifier
    dec_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    dec_model.fit(X_train, y_dec_train)
    dec_pred = dec_model.predict(X_test)
    
    dec_acc = accuracy_score(y_dec_test, dec_pred)
    print(f"Governance Decision Classifier Accuracy: {dec_acc * 100:.2f}%")
    dec_report = classification_report(y_dec_test, dec_pred, output_dict=True)
    
    dec_path = os.path.join(MODELS_DIR, "decision_classifier.joblib")
    joblib.dump(dec_model, dec_path)
    print(f"Saved Decision Model to {dec_path}")
    
    # Save feature metadata
    metadata = {
        "feature_cols": feature_cols,
        "classes": list(dec_model.classes_)
    }
    meta_path = os.path.join(MODELS_DIR, "model_metadata.joblib")
    joblib.dump(metadata, meta_path)
    
    return {
        "risk_rmse": rmse,
        "risk_r2": r2,
        "decision_acc": dec_acc,
        "decision_report": dec_report
    }

def main():
    print("Starting FinGuard AI ML Training Pipeline...")
    intent_res = train_intent_classifier()
    risk_res = train_risk_and_decision_models()
    
    summary = {
        "intent_accuracy": intent_res["accuracy"],
        "risk_rmse": risk_res["risk_rmse"],
        "risk_r2": risk_res["risk_r2"],
        "decision_accuracy": risk_res["decision_acc"]
    }
    
    eval_path = os.path.join(EVAL_DIR, "training_summary.json")
    import json
    with open(eval_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nAll models trained successfully! Summary saved to {eval_path}")

if __name__ == "__main__":
    main()
