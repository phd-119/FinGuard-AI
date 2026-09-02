"""
FinGuard AI - Risk Analytics API Routes
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import RiskAssessmentRecord, AgentProposal, Agent

router = APIRouter(prefix="/risk", tags=["Risk Engine & Analytics"])

@router.get("", response_model=Dict[str, Any])
def get_risk_overview(db: Session = Depends(get_db)):
    """
    Get aggregated risk analytics across all proposals, risk distribution, and risk factors.
    """
    records = db.query(RiskAssessmentRecord).order_by(RiskAssessmentRecord.created_at.desc()).all()
    
    total = len(records)
    high_critical = sum(1 for r in records if r.risk_level in ["HIGH", "CRITICAL"])
    medium = sum(1 for r in records if r.risk_level == "MEDIUM")
    low = sum(1 for r in records if r.risk_level == "LOW")
    avg_score = round(sum(r.risk_score for r in records) / max(1, total), 1)

    recent_assessments = []
    for r in records[:10]:
        proposal = db.query(AgentProposal).filter(AgentProposal.id == r.proposal_id).first()
        agent = db.query(Agent).filter(Agent.id == proposal.agent_id).first() if proposal else None
        recent_assessments.append({
            "proposal_id": r.proposal_id,
            "agent_name": agent.name if agent else "Unknown",
            "amount": proposal.amount if proposal else 0.0,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "risk_factors": r.risk_factors,
            "explanation": r.explanation,
            "created_at": r.created_at
        })

    return {
        "total_assessments": total,
        "high_critical_count": high_critical,
        "medium_count": medium,
        "low_count": low,
        "average_risk_score": avg_score,
        "system_status": "PROTECTED",
        "recent_assessments": recent_assessments
    }
