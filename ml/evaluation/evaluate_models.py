"""
FinGuard AI - ML Model Evaluation & Inference Benchmark
"""

import os
import joblib
import pandas as pd
import numpy as np

ML_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(ML_DIR, "models")
DATA_DIR = os.path.join(ML_DIR, "data")

def evaluate_models():
    intent_model_path = os.path.join(MODELS_DIR, "intent_classifier.joblib")
    risk_model_path = os.path.join(MODELS_DIR, "risk_scorer.joblib")
    dec_model_path = os.path.join(MODELS_DIR, "decision_classifier.joblib")
    meta_path = os.path.join(MODELS_DIR, "model_metadata.joblib")
    
    if not (os.path.exists(intent_model_path) and os.path.exists(risk_model_path)):
        print("Models not found. Run train_models.py first.")
        return
        
    intent_pipeline = joblib.load(intent_model_path)
    risk_model = joblib.load(risk_model_path)
    dec_model = joblib.load(dec_model_path)
    metadata = joblib.load(meta_path)
    
    # Test intent sample
    test_text = ["Payout Agent Payment for supplier raw materials batch #5012"]
    intent_pred = intent_pipeline.predict(test_text)[0]
    intent_proba = np.max(intent_pipeline.predict_proba(test_text))
    print(f"Sample Intent Test: '{test_text[0]}' -> Pred: {intent_pred} (Confidence: {intent_proba:.2%})")
    
    # Test risk sample (Hero demo setup)
    # Available 6L, Reserve 5L, Amount 4L, Concurrent 3L
    hero_features = pd.DataFrame([{
        "amount": 400000.0,
        "available_cash": 600000.0,
        "required_reserve": 500000.0,
        "pending_concurrent_outflows": 300000.0, # 2L growth + 1L refund
        "agent_trust_score": 85.0,
        "agent_confidence": 0.92,
        "policy_violations": 1,
        "urgency_score": 3.0,
        "liquidity_ratio_before": 1.2,
        "projected_liquidity_ratio": 0.4,
        "global_projected_liquidity_ratio": -0.2,
        "reserve_shortfall": 600000.0,
        "cross_agent_conflict_severity": 0.95
    }])[metadata["feature_cols"]]
    
    pred_risk = risk_model.predict(hero_features)[0]
    pred_dec = dec_model.predict(hero_features)[0]
    dec_probas = dec_model.predict_proba(hero_features)[0]
    
    print(f"Hero Scenario ML Inference: Predicted Risk Score = {pred_risk:.1f}/100, Predicted Decision = {pred_dec}")
    print(f"Decision Probabilities: {dict(zip(dec_model.classes_, [round(p, 3) for p in dec_probas]))}")

if __name__ == "__main__":
    evaluate_models()
