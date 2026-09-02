"""
FinGuard AI - Financial Intent Engine
Extracts, classifies, and interprets the real financial intent, operational purpose, and cashflow impact.
"""

from typing import Dict, Any
from app.models.models import AgentProposal, Agent
from app.schemas.schemas import IntentClassificationResult
from app.services.ml_service import ml_service

class IntentEngine:
    def evaluate(self, proposal: AgentProposal, agent: Agent) -> IntentClassificationResult:
        intent_label, purpose, confidence = ml_service.classify_intent(
            agent_name=agent.name,
            description=proposal.reason
        )

        financial_effect_map = {
            "SUPPLIER_SETTLEMENT": "IMMEDIATE_CASH_OUTFLOW",
            "CUSTOMER_REFUND": "IMMEDIATE_CASH_OUTFLOW",
            "GROWTH_INVESTMENT": "DISCRETIONARY_CASH_OUTFLOW",
            "DEBT_COLLECTION": "EXPECTED_CASH_INFLOW",
            "LIQUIDITY_REBALANCE": "INTERNAL_TREASURY_TRANSFER"
        }

        financial_effect = financial_effect_map.get(intent_label, "CASH_OUTFLOW")

        explanation = (
            f"Intent classified as '{intent_label}' ({purpose}) with {confidence * 100:.1f}% confidence. "
            f"Financial impact vector represents a {financial_effect.replace('_', ' ').lower()} "
            f"with urgency level {proposal.urgency}."
        )

        # Update proposal entity with intent insights
        proposal.intent_label = intent_label
        proposal.intent_purpose = purpose
        proposal.intent_confidence = confidence

        return IntentClassificationResult(
            intent_label=intent_label,
            purpose=purpose,
            urgency=proposal.urgency,
            financial_effect=financial_effect,
            confidence=confidence,
            explanation=explanation
        )

intent_engine = IntentEngine()
