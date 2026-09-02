"""
FinGuard AI - Cross-Agent Conflict Engine
THE CORE INNOVATION: Global Multi-Agent Financial Governance.
Detects when multiple independent, uncoordinated AI agents submit proposals that
are individually rational but collectively create severe liquidity or reserve shortfalls.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import AgentProposal, FinancialState, Agent
from app.schemas.schemas import ConflictDetectionResult

class ConflictEngine:
    def detect_conflicts(
        self,
        db: Session,
        current_proposal: AgentProposal,
        state: FinancialState
    ) -> ConflictDetectionResult:
        
        # 1. Retrieve all concurrent pending or proposed actions from OTHER agents
        # (Exclude the current proposal itself and already rejected/executed actions)
        concurrent_proposals = db.query(AgentProposal).filter(
            AgentProposal.id != current_proposal.id,
            AgentProposal.merchant_id == current_proposal.merchant_id,
            AgentProposal.status.in_(["PROPOSED", "AWAITING_APPROVAL", "APPROVED"])
        ).all()

        detected_agents = []
        aggregate_outflow = current_proposal.amount
        
        # Add current proposal
        agent_current = db.query(Agent).filter(Agent.id == current_proposal.agent_id).first()
        detected_agents.append({
            "agent_id": current_proposal.agent_id,
            "agent_name": agent_current.name if agent_current else current_proposal.agent_id,
            "action_type": current_proposal.action_type,
            "amount": current_proposal.amount,
            "urgency": current_proposal.urgency,
            "priority": current_proposal.priority,
            "reason": current_proposal.reason,
            "is_current_subject": True
        })

        for p in concurrent_proposals:
            p_agent = db.query(Agent).filter(Agent.id == p.agent_id).first()
            aggregate_outflow += p.amount
            detected_agents.append({
                "agent_id": p.agent_id,
                "agent_name": p_agent.name if p_agent else p.agent_id,
                "action_type": p.action_type,
                "amount": p.amount,
                "urgency": p.urgency,
                "priority": p.priority,
                "reason": p.reason,
                "is_current_subject": False
            })

        available_cash = state.cash_balance
        required_reserve = state.reserve_requirement
        projected_post_cash = available_cash - aggregate_outflow
        projected_shortfall = max(0.0, required_reserve - projected_post_cash)

        # Conflict Evaluation Logic
        conflict_detected = False
        conflict_type = "NONE"
        severity = "LOW"
        explanation = "No cross-agent liquidity or timing conflicts detected. Financial buffers are adequate."

        if len(detected_agents) > 1:
            if projected_post_cash < required_reserve:
                conflict_detected = True
                conflict_type = "GLOBAL_LIQUIDITY_RESERVE_BREACH"
                severity = "CRITICAL" if projected_post_cash < 0 else "HIGH"
                agent_summary = ", ".join([f"{a['agent_name']} (₹{a['amount']:,.0f})" for a in detected_agents])
                explanation = (
                    f"CRITICAL GLOBAL CONFLICT DETECTED: Multiple autonomous agents ({agent_summary}) "
                    f"are proposing simultaneous financial outflows totaling ₹{aggregate_outflow:,.2f}. "
                    f"With merchant cash at ₹{available_cash:,.2f} and mandatory reserve at ₹{required_reserve:,.2f}, "
                    f"executing these concurrent uncoordinated actions would cause a ₹{projected_shortfall:,.2f} "
                    f"reserve shortfall, threatening insolvency."
                )
            elif aggregate_outflow > (available_cash - required_reserve) * 0.85:
                conflict_detected = True
                conflict_type = "ELEVATED_CONCURRENT_PRESSURE"
                severity = "MEDIUM"
                explanation = (
                    f"CONCURRENT OUTFLOW WARNING: Simultaneous actions across {len(detected_agents)} agents "
                    f"consume {aggregate_outflow / (available_cash - required_reserve) * 100:.1f}% of free unreserved liquidity."
                )

        return ConflictDetectionResult(
            conflict_detected=conflict_detected,
            conflict_type=conflict_type,
            severity=severity,
            detected_agents=detected_agents,
            aggregate_outflow=aggregate_outflow,
            available_cash=available_cash,
            required_reserve=required_reserve,
            projected_shortfall=projected_shortfall,
            explanation=explanation
        )

conflict_engine = ConflictEngine()
