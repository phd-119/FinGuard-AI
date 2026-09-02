"""
FinGuard AI - ML Service Layer
Loads trained ML models and provides inference with statistical fallback mechanisms.
"""

import os
import logging
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from app.core.config import settings

logger = logging.getLogger("finguard.ml")

class MLService:
    def __init__(self):
        self.models_dir = settings.ML_MODELS_DIR
        self.intent_pipeline = None
        self.risk_model = None
        self.decision_model = None
        self.metadata = None
        self._load_models()

    def _load_models(self):
        try:
            intent_path = os.path.join(self.models_dir, "intent_classifier.joblib")
            risk_path = os.path.join(self.models_dir, "risk_scorer.joblib")
            dec_path = os.path.join(self.models_dir, "decision_classifier.joblib")
            meta_path = os.path.join(self.models_dir, "model_metadata.joblib")

            if os.path.exists(intent_path):
                self.intent_pipeline = joblib.load(intent_path)
                logger.info("Loaded Intent Classification Model")
            if os.path.exists(risk_path):
                self.risk_model = joblib.load(risk_path)
                logger.info("Loaded Multi-Factor Risk Model")
            if os.path.exists(dec_path):
                self.decision_model = joblib.load(dec_path)
                logger.info("Loaded Decision Classifier Model")
            if os.path.exists(meta_path):
                self.metadata = joblib.load(meta_path)
        except Exception as e:
            logger.warning(f"Error loading ML models: {e}. Fallback to deterministic algorithms.")

    def classify_intent(self, agent_name: str, description: str) -> Tuple[str, str, float]:
        """
        Classifies financial intent label, purpose category, and confidence.
        """
        purpose_map = {
            "SUPPLIER_SETTLEMENT": "Operational Obligation (Vendor Payables)",
            "CUSTOMER_REFUND": "Customer Experience & Chargeback Mitigation",
            "GROWTH_INVESTMENT": "Revenue Expansion & Customer Acquisition",
            "DEBT_COLLECTION": "Working Capital Optimization & Receivables Recovery",
            "LIQUIDITY_REBALANCE": "Capital Preservation & Treasury Buffer Management"
        }

        if self.intent_pipeline is not None:
            try:
                feature_text = f"{agent_name} {description}"
                pred = self.intent_pipeline.predict([feature_text])[0]
                probas = self.intent_pipeline.predict_proba([feature_text])[0]
                conf = float(np.max(probas))
                purpose = purpose_map.get(pred, "General Financial Movement")
                return pred, purpose, conf
            except Exception as e:
                logger.warning(f"ML intent inference failed: {e}")

        # Deterministic fallback
        desc_lower = description.lower()
        if "supplier" in desc_lower or "vendor" in desc_lower or "invoice" in desc_lower or "payout" in desc_lower:
            return "SUPPLIER_SETTLEMENT", purpose_map["SUPPLIER_SETTLEMENT"], 0.94
        elif "refund" in desc_lower or "chargeback" in desc_lower or "return" in desc_lower or "damaged" in desc_lower:
            return "CUSTOMER_REFUND", purpose_map["CUSTOMER_REFUND"], 0.96
        elif "ad spend" in desc_lower or "marketing" in desc_lower or "campaign" in desc_lower or "growth" in desc_lower:
            return "GROWTH_INVESTMENT", purpose_map["GROWTH_INVESTMENT"], 0.93
        elif "receivable" in desc_lower or "debt" in desc_lower or "collection" in desc_lower:
            return "DEBT_COLLECTION", purpose_map["DEBT_COLLECTION"], 0.91
        else:
            return "LIQUIDITY_REBALANCE", purpose_map["LIQUIDITY_REBALANCE"], 0.88

    def predict_risk_and_decision(self, features: Dict[str, Any]) -> Tuple[float, str, str, float]:
        """
        Predicts continuous risk score (0-100), risk category, ML recommended decision, and confidence.
        """
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

        if self.risk_model is not None and self.decision_model is not None:
            try:
                df = pd.DataFrame([features])[feature_cols]
                risk_score = float(self.risk_model.predict(df)[0])
                risk_score = float(np.clip(risk_score, 1.0, 99.0))
                
                dec_pred = self.decision_model.predict(df)[0]
                dec_probas = self.decision_model.predict_proba(df)[0]
                conf = float(np.max(dec_probas))
                
                if risk_score >= 80.0:
                    category = "CRITICAL"
                elif risk_score >= 60.0:
                    category = "HIGH"
                elif risk_score >= 35.0:
                    category = "MEDIUM"
                else:
                    category = "LOW"
                    
                return risk_score, category, dec_pred, conf
            except Exception as e:
                logger.warning(f"ML risk inference failed: {e}")

        # Deterministic Statistical Fallback
        amt = features.get("amount", 0.0)
        cash = max(1.0, features.get("available_cash", 1.0))
        reserve = max(1.0, features.get("required_reserve", 1.0))
        concurrent = features.get("pending_concurrent_outflows", 0.0)
        violations = features.get("policy_violations", 0)
        trust = features.get("agent_trust_score", 85.0)
        conflict_sev = features.get("cross_agent_conflict_severity", 0.0)
        
        total_out = amt + concurrent
        shortfall = max(0.0, reserve - (cash - total_out))
        
        f_reserve = min(40.0, (shortfall / reserve) * 40.0) if shortfall > 0 else (total_out / cash) * 15.0
        f_amt = min(25.0, (amt / max(1.0, cash - reserve)) * 25.0)
        f_conflict = conflict_sev * 20.0
        f_policy = violations * 6.0
        f_trust = (80.0 - trust) * 0.2
        
        score = float(np.clip(f_reserve + f_amt + f_conflict + f_policy + f_trust, 5.0, 95.0))
        
        if score >= 80.0:
            category = "CRITICAL"
        elif score >= 60.0:
            category = "HIGH"
        elif score >= 35.0:
            category = "MEDIUM"
        else:
            category = "LOW"
            
        if violations >= 2 or (cash - amt) < 0:
            decision = "BLOCK"
        elif conflict_sev > 0.5 or (shortfall > 0 and amt > 100000):
            decision = "MODIFY"
        elif score >= 70.0:
            decision = "ESCALATE"
        else:
            decision = "ALLOW"
            
        return score, category, decision, 0.92

ml_service = MLService()
