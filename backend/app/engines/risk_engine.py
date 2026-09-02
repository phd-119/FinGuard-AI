"""
FinGuard AI - Risk Assessment Engine
Synthesizes multi-factor telemetry, ML risk regression, liquidity threats, and policy compliance.
"""

from typing import List
from app.models.models import AgentProposal, FinancialState, Agent
from app.schemas.schemas import (
    RiskAssessmentResult, PolicyCheckResult, ConflictDetectionResult, FutureImpactResult, AgentTrustResult
)
from app.services.ml_service import ml_service

class RiskEngine:
    def assess_risk(
        self,
        proposal: AgentProposal,
        state: FinancialState,
        agent: Agent,
        policy_checks: List[PolicyCheckResult],
        conflict: ConflictDetectionResult,
        future_impact: FutureImpactResult,
        trust: AgentTrustResult
    ) -> RiskAssessmentResult:
        
        # Count policy violations
        violations = sum(1 for p in policy_checks if not p.is_compliant)
        
        # Urgency score mapping
        urgency_map = {"LOW": 1.0, "MEDIUM": 2.0, "HIGH": 3.0, "CRITICAL": 4.0}
        urgency_score = urgency_map.get(proposal.urgency, 2.0)

        # Conflict severity mapping
        conflict_sev_map = {"NONE": 0.0, "LOW": 0.15, "MEDIUM": 0.45, "HIGH": 0.80, "CRITICAL": 0.98}
        conflict_sev = conflict_sev_map.get(conflict.severity, 0.0)

        # Feature vector for ML Regressor
        liquidity_before = state.cash_balance / max(1.0, state.reserve_requirement)
        total_outflow = conflict.aggregate_outflow if conflict.conflict_detected else proposal.amount
        global_proj_ratio = max(-0.5, (state.cash_balance - total_outflow) / max(1.0, state.reserve_requirement))

        features = {
            "amount": proposal.amount,
            "available_cash": state.cash_balance,
            "required_reserve": state.reserve_requirement,
            "pending_concurrent_outflows": max(0.0, conflict.aggregate_outflow - proposal.amount),
            "agent_trust_score": agent.trust_score,
            "agent_confidence": proposal.confidence,
            "policy_violations": violations,
            "urgency_score": urgency_score,
            "liquidity_ratio_before": liquidity_before,
            "projected_liquidity_ratio": future_impact.projected_liquidity_ratio,
            "global_projected_liquidity_ratio": global_proj_ratio,
            "reserve_shortfall": future_impact.reserve_shortfall,
            "cross_agent_conflict_severity": conflict_sev
        }

        risk_score, risk_level, ml_decision, model_conf = ml_service.predict_risk_and_decision(features)

        # Compile detailed risk factors
        risk_factors = []
        if future_impact.reserve_shortfall > 0:
            risk_factors.append(f"Projected statutory reserve breach of ₹{future_impact.reserve_shortfall:,.2f}")
        if conflict.conflict_detected:
            risk_factors.append(f"High multi-agent concurrency pressure across {len(conflict.detected_agents)} agents (₹{conflict.aggregate_outflow:,.2f} total)")
        if proposal.amount > (state.cash_balance - state.reserve_requirement):
            risk_factors.append(f"Proposal exceeds unreserved free cash buffer (₹{state.cash_balance - state.reserve_requirement:,.2f})")
        if violations > 0:
            risk_factors.append(f"Detected {violations} financial governance policy violation(s)")
        if agent.trust_score < 75.0:
            risk_factors.append(f"Agent historical trust score ({agent.trust_score:.1f}) requires enhanced governance oversight")
        if proposal.urgency in ["HIGH", "CRITICAL"]:
            risk_factors.append(f"Elevated proposal urgency: {proposal.urgency}")

        if not risk_factors:
            risk_factors.append("Nominal operational transaction within all safe liquidity bounds.")

        explanation = (
            f"Multi-Factor Risk Score evaluated at {risk_score:.1f}/100 ({risk_level} Risk). "
            f"Primary risk drivers: {'; '.join(risk_factors[:3])}."
        )

        return RiskAssessmentResult(
            risk_score=risk_score,
            risk_level=risk_level,
            risk_factors=risk_factors,
            model_confidence=model_conf,
            explanation=explanation
        )

risk_engine = RiskEngine()
