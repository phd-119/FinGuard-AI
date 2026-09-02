"""
FinGuard AI - Actions & Action Gateway API Routes
The central routing for proposing, evaluating, deciding, and executing agent actions.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import (
    AgentProposal, Agent, FinancialState, ConflictRecord, RiskAssessmentRecord,
    FutureImpactRecord, SimulationRecord, DecisionRecord, HumanApprovalRecord, ExecutionRecord, AuditRecord
)
from app.schemas.schemas import (
    ProposeActionRequest, EvaluationPipelineResponse, ProposalSummaryOut,
    GovernanceDecisionResult, ExecutionResultOut
)
from app.engines.action_gateway import action_gateway
from app.services.governance_pipeline import governance_pipeline
from app.execution.simulator import execution_simulator

router = APIRouter(prefix="/actions", tags=["Action Gateway & Decision Pipeline"])

@router.post("/propose", response_model=EvaluationPipelineResponse)
@router.post("/propose/{merchant_id}", response_model=EvaluationPipelineResponse)
def propose_and_evaluate_action(
    req: ProposeActionRequest,
    merchant_id: Optional[str] = None,
    auto_evaluate: bool = True,
    db: Session = Depends(get_db)
):
    """
    ACTION GATEWAY ENTRYPOINT:
    Autonomous AI Agent submits a proposed financial action.
    The proposal is intercepted, validated, and evaluated through the 10-stage FinGuard pipeline.
    """
    if merchant_id and not req.merchant_id:
        req.merchant_id = merchant_id
        
    proposal = action_gateway.validate_and_ingest(db, req)
    result = governance_pipeline.evaluate_proposal(db, proposal.id)
    return result


@router.get("", response_model=List[ProposalSummaryOut])
@router.get("/", response_model=List[ProposalSummaryOut])
def list_proposals(
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all pending and historical financial proposals across agents.
    """
    query = db.query(AgentProposal).order_by(AgentProposal.created_at.desc())
    if agent_id:
        query = query.filter(AgentProposal.agent_id == agent_id)
    if status:
        query = query.filter(AgentProposal.status == status)
        
    proposals = query.all()
    results = []
    for p in proposals:
        agent = db.query(Agent).filter(Agent.id == p.agent_id).first()
        risk_score = p.risk_assessment.risk_score if p.risk_assessment else None
        risk_level = p.risk_assessment.risk_level if p.risk_assessment else None
        conflict_sev = p.conflict.severity if p.conflict and p.conflict.conflict_detected else "NONE"
        
        results.append(ProposalSummaryOut(
            id=p.id,
            agent_id=p.agent_id,
            agent_name=agent.name if agent else p.agent_id,
            action_type=p.action_type,
            amount=p.amount,
            currency=p.currency,
            urgency=p.urgency,
            priority=p.priority,
            status=p.status,
            final_decision=p.final_decision,
            risk_score=risk_score,
            risk_level=risk_level,
            conflict_severity=conflict_sev,
            reason=p.reason,
            created_at=p.created_at
        ))
    return results


@router.get("/status/{action_id}", response_model=EvaluationPipelineResponse)
@router.get("/{action_id}", response_model=EvaluationPipelineResponse)
def get_action_reasoning_flow(action_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the complete, transparent 10-stage reasoning flow and telemetry for an action.
    """
    proposal = db.query(AgentProposal).filter(AgentProposal.id == action_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Action proposal '{action_id}' not found.")

    return governance_pipeline.evaluate_proposal(db, proposal.id)


@router.post("/{action_id}/evaluate", response_model=EvaluationPipelineResponse)
def evaluate_action(action_id: str, db: Session = Depends(get_db)):
    """
    Trigger or re-trigger the complete 10-stage FinGuard Governance Pipeline for an action.
    """
    return governance_pipeline.evaluate_proposal(db, action_id)


@router.get("/{action_id}/decision", response_model=GovernanceDecisionResult)
def get_action_decision(action_id: str, db: Session = Depends(get_db)):
    """
    Get the standalone governance decision (ALLOW / MODIFY / DELAY / ESCALATE / BLOCK).
    """
    proposal = db.query(AgentProposal).filter(AgentProposal.id == action_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Action proposal '{action_id}' not found.")
    
    if not proposal.decision_record:
        eval_res = governance_pipeline.evaluate_proposal(db, proposal.id)
        return eval_res.decision
    
    dec = proposal.decision_record
    return GovernanceDecisionResult(
        decision=dec.decision,
        decision_reason=dec.decision_reason,
        recommended_action=dec.recommended_action,
        modified_amount=dec.modified_amount,
        deferred_amount=dec.deferred_amount,
        delay_hours=dec.delay_hours,
        risk_level=dec.risk_level,
        confidence=dec.confidence,
        supporting_factors=dec.supporting_factors or [],
        requires_human_approval=dec.requires_human_approval
    )


@router.post("/execute/{action_id}", response_model=ExecutionResultOut)
@router.post("/{action_id}/execute", response_model=ExecutionResultOut)
def execute_action(action_id: str, db: Session = Depends(get_db)):
    """
    Simulated Execution Endpoint:
    Only executes if the proposal is in ALLOWED or APPROVED status.
    Direct execution without prior FinGuard evaluation is strictly blocked.
    """
    proposal = db.query(AgentProposal).filter(AgentProposal.id == action_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Action proposal '{action_id}' not found.")

    if proposal.status == "EXECUTED":
        raise HTTPException(status_code=400, detail="Action has already been executed.")

    if proposal.final_decision == "BLOCK" or proposal.status == "BLOCKED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Execution Rejection: FinGuard has BLOCKED this financial action for severe policy violations."
        )

    # Determine executable amount
    exec_amount = proposal.amount
    if proposal.decision_record and proposal.decision_record.modified_amount is not None:
        exec_amount = proposal.decision_record.modified_amount

    # Execute safely via simulator
    res = execution_simulator.execute_governed_action(
        db=db,
        proposal=proposal,
        approved_amount=exec_amount,
        human_approver="FinGuard Automated Execution Layer",
        approval_comment=proposal.decision_record.decision_reason if proposal.decision_record else "Governed execution"
    )
    return res
