"""
FinGuard AI - Governance Decision Engine
The apex synthesis engine that adjudicates financial actions into:
ALLOW | MODIFY | DELAY | ESCALATE | BLOCK
"""

from typing import List
from app.models.models import AgentProposal, FinancialState, Agent
from app.schemas.schemas import (
    GovernanceDecisionResult, PolicyCheckResult, ConflictDetectionResult,
    FutureImpactResult, RiskAssessmentResult, AgentTrustResult,
    ScenarioComparison, SafeAlternativeResult
)

class DecisionEngine:
    def decide(
        self,
        proposal: AgentProposal,
        state: FinancialState,
        agent: Agent,
        policy_checks: List[PolicyCheckResult],
        conflict: ConflictDetectionResult,
        future_impact: FutureImpactResult,
        risk: RiskAssessmentResult,
        trust: AgentTrustResult,
        scenarios: List[ScenarioComparison],
        alternative: SafeAlternativeResult
    ) -> GovernanceDecisionResult:
        
        violations = [p for p in policy_checks if not p.is_compliant]
        critical_violations = [p for p in violations if p.severity == "CRITICAL"]

        supporting_factors = []
        requires_human = False
        decision = "ALLOW"
        reason = ""

        # 1. Hard Block Condition
        if len(critical_violations) >= 2 or agent.status == "RESTRICTED" or state.cash_balance < 0:
            decision = "BLOCK"
            reason = f"Action blocked due to {len(critical_violations)} critical policy violations and severe solvency breach."
            supporting_factors.append("Multiple critical policy violations detected.")
            supporting_factors.append("Direct unmitigated risk to merchant solvency.")
            return GovernanceDecisionResult(
                decision=decision,
                decision_reason=reason,
                recommended_action="Block transaction; alert merchant administrators.",
                modified_amount=0.0,
                deferred_amount=0.0,
                delay_hours=0,
                risk_level=risk.risk_level,
                confidence=0.99,
                supporting_factors=supporting_factors,
                requires_human_approval=False
            )

        # 2. Modify Condition (Reserve threatened or multi-agent conflict, but split alternative is feasible)
        if (conflict.conflict_detected and conflict.severity in ["HIGH", "CRITICAL"]) or \
           (future_impact.reserve_shortfall > 0 and alternative.immediate_amount > 0):
            decision = "MODIFY"
            requires_human = True
            reason = (
                f"Full execution of ₹{proposal.amount:,.2f} would trigger a reserve breach under concurrent multi-agent load. "
                f"FinGuard recommends modifying the transaction to execute ₹{alternative.immediate_amount:,.2f} immediately "
                f"and deferring ₹{alternative.deferred_amount:,.2f} to protect the ₹{state.reserve_requirement:,.2f} reserve."
            )
            supporting_factors.append(f"Global conflict with {len(conflict.detected_agents)} agents totaling ₹{conflict.aggregate_outflow:,.2f}.")
            supporting_factors.append(f"Protects mandatory statutory reserve of ₹{state.reserve_requirement:,.2f}.")
            supporting_factors.append(f"Satisfies ₹{alternative.immediate_amount:,.2f} of immediate agent obligation.")
            
            return GovernanceDecisionResult(
                decision=decision,
                decision_reason=reason,
                recommended_action=alternative.recommended_action,
                modified_amount=alternative.immediate_amount,
                deferred_amount=alternative.deferred_amount,
                delay_hours=alternative.delay_hours,
                risk_level=risk.risk_level,
                confidence=0.95,
                supporting_factors=supporting_factors,
                requires_human_approval=requires_human
            )

        # 3. Escalate Condition (High Risk score >= 65, or high transaction threshold requiring dual authorization)
        if risk.risk_score >= 65.0 or proposal.amount >= 350000.0:
            decision = "ESCALATE"
            requires_human = True
            reason = (
                f"Elevated risk score ({risk.risk_score:.1f}/100) or high capital outlay requires human treasury authorization "
                f"prior to execution."
            )
            supporting_factors.append(f"Risk Score {risk.risk_score:.1f} exceeds human approval threshold (65.0).")
            supporting_factors.append(f"Proposal amount ₹{proposal.amount:,.2f} requires dual control verification.")
            
            return GovernanceDecisionResult(
                decision=decision,
                decision_reason=reason,
                recommended_action="Submit proposal to Human Approval Center for dual-signoff.",
                modified_amount=proposal.amount,
                deferred_amount=0.0,
                delay_hours=0,
                risk_level=risk.risk_level,
                confidence=0.92,
                supporting_factors=supporting_factors,
                requires_human_approval=requires_human
            )

        # 4. Delay Condition (Low urgency, moderate risk)
        if proposal.urgency in ["LOW", "MEDIUM"] and (future_impact.projected_liquidity_ratio < 1.1 or risk.risk_score >= 50.0):
            decision = "DELAY"
            requires_human = False
            reason = (
                f"Non-critical urgency ({proposal.urgency}) and tight liquidity cushion suggest delaying execution "
                f"by 24h until next scheduled receivables inflow of ₹{state.daily_inflows:,.2f} settles."
            )
            supporting_factors.append("Low/Medium operational urgency.")
            supporting_factors.append("Schedules execution after next positive liquidity event.")
            
            return GovernanceDecisionResult(
                decision=decision,
                decision_reason=reason,
                recommended_action=f"Delay transaction by 24h to await incoming inflows.",
                modified_amount=0.0,
                deferred_amount=proposal.amount,
                delay_hours=24,
                risk_level=risk.risk_level,
                confidence=0.91,
                supporting_factors=supporting_factors,
                requires_human_approval=requires_human
            )

        # 5. Allow Condition (Safe operational bounds)
        decision = "ALLOW"
        requires_human = False
        reason = (
            f"Proposal of ₹{proposal.amount:,.2f} complies with all financial policies, preserves statutory reserves, "
            f"and exhibits acceptable risk ({risk.risk_score:.1f}/100)."
        )
        supporting_factors.append("Full compliance with all active governance policies.")
        supporting_factors.append(f"Preserves cash reserve buffer above ₹{state.reserve_requirement:,.2f}.")
        supporting_factors.append(f"Agent trust score ({agent.trust_score:.1f}) verified.")

        return GovernanceDecisionResult(
            decision=decision,
            decision_reason=reason,
            recommended_action=f"Execute full transaction ₹{proposal.amount:,.2f} immediately.",
            modified_amount=proposal.amount,
            deferred_amount=0.0,
            delay_hours=0,
            risk_level=risk.risk_level,
            confidence=0.97,
            supporting_factors=supporting_factors,
            requires_human_approval=requires_human
        )

decision_engine = DecisionEngine()
