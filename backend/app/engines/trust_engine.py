"""
FinGuard AI - Agent Trust Engine
Evaluates dynamic trust, reliability telemetry, and historical compliance of autonomous AI agents.
"""

from typing import List
from sqlalchemy.orm import Session
from app.models.models import Agent, AgentProposal
from app.schemas.schemas import AgentTrustResult

class TrustEngine:
    def evaluate(self, db: Session, agent: Agent) -> AgentTrustResult:
        total = max(1, agent.total_proposals)
        violations = agent.violation_count
        violation_rate = round(violations / total, 3)

        factors = []
        
        # 1. Base trust score adjustment based on telemetry
        if agent.trust_score >= 85.0:
            level = "HIGH"
            factors.append("Strong historical compliance with zero critical policy breaches.")
        elif agent.trust_score >= 70.0:
            level = "MEDIUM"
            factors.append("Moderate track record with occasional threshold adjustments.")
        elif agent.trust_score >= 50.0:
            level = "LOW"
            factors.append("High volatility in proposed outflow volumes; heightened supervision.")
        else:
            level = "RESTRICTED"
            factors.append("Severe compliance penalties; autonomous execution privileges suspended.")

        if agent.approved_proposals > 10:
            factors.append(f"Successfully executed {agent.approved_proposals} audited transactions.")
        if agent.modified_proposals > 0:
            factors.append(f"Subject to {agent.modified_proposals} automated safe modifications.")
        if violations > 0:
            factors.append(f"Recorded {violations} historical limit violations.")

        return AgentTrustResult(
            agent_id=agent.id,
            trust_score=agent.trust_score,
            trust_level=level,
            historical_proposals=agent.total_proposals,
            violation_rate=violation_rate,
            factors=factors
        )

    def record_outcome(self, db: Session, agent: Agent, outcome: str, violation: bool = False):
        """
        Updates dynamic trust score following a governed action outcome.
        """
        if outcome == "ALLOW":
            agent.approved_proposals += 1
            agent.trust_score = min(99.0, agent.trust_score + 0.5)
        elif outcome == "MODIFY":
            agent.modified_proposals += 1
            # Modifying is a positive cooperative adaptation, slight boost/neutral
            agent.trust_score = min(99.0, agent.trust_score + 0.2)
        elif outcome == "BLOCK":
            agent.blocked_proposals += 1
            agent.trust_score = max(20.0, agent.trust_score - 3.0)
            
        if violation:
            agent.violation_count += 1
            agent.trust_score = max(15.0, agent.trust_score - 5.0)

        # Update trust level
        if agent.trust_score >= 80:
            agent.trust_level = "HIGH"
        elif agent.trust_score >= 60:
            agent.trust_level = "MEDIUM"
        elif agent.trust_score >= 40:
            agent.trust_level = "LOW"
        else:
            agent.trust_level = "RESTRICTED"

        db.commit()

trust_engine = TrustEngine()
