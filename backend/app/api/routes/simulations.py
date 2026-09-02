"""
FinGuard AI - Simulations API Routes
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import SimulationRecord, AgentProposal
from app.schemas.schemas import ScenarioComparison
from app.services.governance_pipeline import governance_pipeline

router = APIRouter(prefix="/simulations", tags=["What-If Simulation Studio"])

@router.get("/{action_id}", response_model=List[ScenarioComparison])
def get_action_simulations(action_id: str, db: Session = Depends(get_db)):
    """
    Retrieve counterfactual What-If scenario simulations for an action proposal.
    """
    proposal = db.query(AgentProposal).filter(AgentProposal.id == action_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Action '{action_id}' not found.")

    sims = db.query(SimulationRecord).filter(SimulationRecord.proposal_id == action_id).all()
    if not sims:
        eval_res = governance_pipeline.evaluate_proposal(db, action_id)
        return eval_res.what_if_scenarios

    return [
        ScenarioComparison(
            scenario_id=s.scenario_id,
            name=s.name,
            description=s.description,
            immediate_outflow=s.immediate_outflow,
            deferred_outflow=s.deferred_outflow,
            remaining_cash=s.remaining_cash,
            reserve_shortfall=s.reserve_shortfall,
            liquidity_ratio=s.liquidity_ratio,
            risk_score=s.risk_score,
            policy_compliant=s.policy_compliant,
            is_recommended=s.is_recommended
        )
        for s in sims
    ]
