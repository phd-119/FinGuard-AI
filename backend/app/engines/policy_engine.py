"""
FinGuard AI - Policy Engine
Evaluates proposals against financial policies, risk limits, liquidity thresholds, and statutory reserve mandates.
"""

from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.models import Policy, AgentProposal, FinancialState, Agent
from app.schemas.schemas import PolicyCheckResult

class PolicyEngine:
    def evaluate(
        self,
        db: Session,
        proposal: AgentProposal,
        state: FinancialState,
        agent: Agent
    ) -> List[PolicyCheckResult]:
        
        policies = db.query(Policy).filter(Policy.is_active == True).all()
        results: List[PolicyCheckResult] = []

        # If no policies in DB yet, fallback to default standard policies
        if not policies:
            # Check 1: Reserve floor
            post_cash = state.cash_balance - proposal.amount
            reserve_ok = post_cash >= state.reserve_requirement
            results.append(PolicyCheckResult(
                policy_code="POL_RESERVE_FLOOR",
                policy_name="Minimum Mandatory Cash Reserve",
                is_compliant=reserve_ok,
                threshold=state.reserve_requirement,
                actual_value=post_cash,
                severity="CRITICAL",
                message=f"Post-execution cash (₹{post_cash:,.2f}) must remain >= reserve requirement (₹{state.reserve_requirement:,.2f})"
                if reserve_ok else f"Violation: Post-execution cash (₹{post_cash:,.2f}) breaches minimum reserve of ₹{state.reserve_requirement:,.2f}"
            ))

            # Check 2: Single Tx limit
            max_single = 500000.0
            single_ok = proposal.amount <= max_single
            results.append(PolicyCheckResult(
                policy_code="POL_MAX_SINGLE_TX",
                policy_name="Maximum Single Transaction Cap",
                is_compliant=single_ok,
                threshold=max_single,
                actual_value=proposal.amount,
                severity="HIGH",
                message=f"Transaction amount ₹{proposal.amount:,.2f} complies with single tx limit of ₹{max_single:,.2f}"
                if single_ok else f"Violation: Transaction amount ₹{proposal.amount:,.2f} exceeds max single limit of ₹{max_single:,.2f}"
            ))

            # Check 3: Trust threshold
            trust_ok = agent.trust_score >= 60.0
            results.append(PolicyCheckResult(
                policy_code="POL_AGENT_TRUST",
                policy_name="Agent Autonomous Trust Baseline",
                is_compliant=trust_ok,
                threshold=60.0,
                actual_value=agent.trust_score,
                severity="HIGH",
                message=f"Agent trust score {agent.trust_score:.1f} is above minimum safety threshold 60.0"
                if trust_ok else f"Warning: Agent trust score {agent.trust_score:.1f} is below autonomous trust requirement 60.0"
            ))

            return results

        # Evaluate against active DB policies
        for pol in policies:
            is_compliant = True
            actual_val = 0.0
            msg = ""

            if pol.code == "POL_RESERVE_FLOOR":
                actual_val = state.cash_balance - proposal.amount
                is_compliant = actual_val >= pol.threshold_value
                msg = f"Projected cash balance after individual proposal is ₹{actual_val:,.2f} (Required: ₹{pol.threshold_value:,.2f})"
                if not is_compliant:
                    msg = f"Breach: Projected cash ₹{actual_val:,.2f} dips below mandatory reserve floor ₹{pol.threshold_value:,.2f}"

            elif pol.code == "POL_MAX_SINGLE_TX":
                actual_val = proposal.amount
                is_compliant = actual_val <= pol.threshold_value
                msg = f"Amount ₹{actual_val:,.2f} <= ₹{pol.threshold_value:,.2f} cap" if is_compliant else f"Amount ₹{actual_val:,.2f} exceeds cap of ₹{pol.threshold_value:,.2f}"

            elif pol.code == "POL_DAILY_PAYOUT_CAP" and proposal.action_type in ["PAYOUT", "VENDOR_SETTLEMENT"]:
                actual_val = state.daily_outflows + proposal.amount
                is_compliant = actual_val <= pol.threshold_value
                msg = f"Cumulative daily payout ₹{actual_val:,.2f} within limit ₹{pol.threshold_value:,.2f}" if is_compliant else f"Daily payout cap ₹{pol.threshold_value:,.2f} exceeded (Projected: ₹{actual_val:,.2f})"

            elif pol.code == "POL_DAILY_REFUND_CAP" and proposal.action_type in ["REFUND", "CHARGEBACK_REVERSAL"]:
                actual_val = state.pending_refunds + proposal.amount
                is_compliant = actual_val <= pol.threshold_value
                msg = f"Cumulative daily refunds ₹{actual_val:,.2f} within cap ₹{pol.threshold_value:,.2f}"

            elif pol.code == "POL_DAILY_GROWTH_CAP" and proposal.action_type in ["MARKETING_SPEND", "AD_BUDGET_ALLOCATION"]:
                actual_val = state.marketing_spend + proposal.amount
                is_compliant = actual_val <= pol.threshold_value
                msg = f"Cumulative marketing spend ₹{actual_val:,.2f} within cap ₹{pol.threshold_value:,.2f}"

            elif pol.code == "POL_AGENT_TRUST":
                actual_val = agent.trust_score
                is_compliant = actual_val >= pol.threshold_value
                msg = f"Agent trust score {actual_val:.1f} meets threshold {pol.threshold_value:.1f}" if is_compliant else f"Agent trust {actual_val:.1f} below threshold {pol.threshold_value:.1f}"

            results.append(PolicyCheckResult(
                policy_code=pol.code,
                policy_name=pol.name,
                is_compliant=is_compliant,
                threshold=pol.threshold_value,
                actual_value=float(actual_val),
                severity=pol.severity,
                message=msg
            ))

        return results

policy_engine = PolicyEngine()
