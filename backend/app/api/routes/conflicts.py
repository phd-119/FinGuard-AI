"""
FinGuard AI - Conflicts API Routes
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ConflictRecord, AgentProposal, FinancialState, Agent
from app.schemas.schemas import ConflictDetectionResult

router = APIRouter(prefix="/conflicts", tags=["Cross-Agent Conflict Engine"])

@router.get("", response_model=List[Dict[str, Any]])
def list_detected_conflicts(db: Session = Depends(get_db)):
    """
    Retrieve all detected cross-agent liquidity and timing conflicts.
    """
    records = db.query(ConflictRecord).filter(ConflictRecord.conflict_detected == True).order_by(ConflictRecord.created_at.desc()).all()
    results = []
    for r in records:
        proposal = db.query(AgentProposal).filter(AgentProposal.id == r.proposal_id).first()
        agent = db.query(Agent).filter(Agent.id == proposal.agent_id).first() if proposal else None
        
        results.append({
            "id": r.id,
            "proposal_id": r.proposal_id,
            "agent_id": proposal.agent_id if proposal else "unknown",
            "agent_name": agent.name if agent else "Unknown",
            "action_type": proposal.action_type if proposal else "UNKNOWN",
            "proposed_amount": proposal.amount if proposal else 0.0,
            "conflict_type": r.conflict_type,
            "severity": r.severity,
            "detected_agents": r.detected_agents,
            "aggregate_outflow": r.aggregate_outflow,
            "available_cash": r.available_cash,
            "required_reserve": r.required_reserve,
            "projected_shortfall": r.projected_shortfall,
            "explanation": r.explanation,
            "created_at": r.created_at
        })
    return results
