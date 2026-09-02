"""
FinGuard AI - Human Approval Center API Routes
Enforces dual control and human signoff for high-risk, escalated, or modified financial decisions.
"""

from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import AgentProposal, HumanApprovalRecord, Agent, DecisionRecord
from app.schemas.schemas import HumanApprovalRequest, ExecutionResultOut
from app.execution.simulator import execution_simulator

router = APIRouter(prefix="/approvals", tags=["Human Approval Center"])

@router.get("", response_model=List[Dict[str, Any]])
def list_pending_approvals(db: Session = Depends(get_db)):
    """
    List all autonomous agent proposals currently awaiting human treasury approval.
    """
    approvals = db.query(HumanApprovalRecord).filter(HumanApprovalRecord.status == "PENDING").all()
    results = []
    for a in approvals:
        proposal = db.query(AgentProposal).filter(AgentProposal.id == a.proposal_id).first()
        if not proposal:
            continue
        agent = db.query(Agent).filter(Agent.id == proposal.agent_id).first()
        dec = proposal.decision_record

        results.append({
            "approval_id": a.id,
            "proposal_id": proposal.id,
            "agent_id": proposal.agent_id,
            "agent_name": agent.name if agent else proposal.agent_id,
            "action_type": proposal.action_type,
            "original_amount": proposal.amount,
            "recommended_amount": dec.modified_amount if dec and dec.modified_amount is not None else proposal.amount,
            "deferred_amount": dec.deferred_amount if dec else 0.0,
            "governance_decision": dec.decision if dec else "ESCALATE",
            "decision_reason": dec.decision_reason if dec else "Awaiting human review",
            "risk_score": proposal.risk_assessment.risk_score if proposal.risk_assessment else 75.0,
            "risk_level": proposal.risk_assessment.risk_level if proposal.risk_assessment else "HIGH",
            "conflict_detected": proposal.conflict.conflict_detected if proposal.conflict else False,
            "requested_at": a.requested_at,
            "comments": a.comments
        })
    return results

@router.post("/{action_id}/approve", response_model=ExecutionResultOut)
def approve_action(
    action_id: str,
    req: HumanApprovalRequest,
    db: Session = Depends(get_db)
):
    """
    Human Reviewer signs off on the proposal.
    Executes either the recommended governed amount or specified override amount,
    updates the financial state, and mints an audit receipt.
    """
    proposal = db.query(AgentProposal).filter(AgentProposal.id == action_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Proposal '{action_id}' not found.")

    if proposal.status == "EXECUTED":
        raise HTTPException(status_code=400, detail="Action already executed.")

    appr = db.query(HumanApprovalRecord).filter(HumanApprovalRecord.proposal_id == action_id).first()
    if not appr:
        appr = HumanApprovalRecord(proposal_id=action_id)
        db.add(appr)

    # Determine execution amount
    exec_amount = req.approved_amount
    if exec_amount is None:
        if proposal.decision_record and proposal.decision_record.modified_amount is not None:
            exec_amount = proposal.decision_record.modified_amount
        else:
            exec_amount = proposal.amount

    appr.human_reviewer = req.human_reviewer
    appr.status = "APPROVED"
    appr.approved_amount = exec_amount
    appr.comments = req.comments or "Approved via FinGuard Control Plane."
    appr.reviewed_at = datetime.utcnow()
    proposal.status = "APPROVED"
    db.commit()

    # Trigger safe simulated execution
    result = execution_simulator.execute_governed_action(
        db=db,
        proposal=proposal,
        approved_amount=exec_amount,
        human_approver=req.human_reviewer,
        approval_comment=appr.comments
    )
    return result

@router.post("/{action_id}/reject", response_model=Dict[str, Any])
def reject_action(
    action_id: str,
    req: HumanApprovalRequest,
    db: Session = Depends(get_db)
):
    """
    Human Reviewer rejects the proposal.
    Cancels execution and records the decision in the audit log.
    """
    proposal = db.query(AgentProposal).filter(AgentProposal.id == action_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail=f"Proposal '{action_id}' not found.")

    appr = db.query(HumanApprovalRecord).filter(HumanApprovalRecord.proposal_id == action_id).first()
    if not appr:
        appr = HumanApprovalRecord(proposal_id=action_id)
        db.add(appr)

    appr.human_reviewer = req.human_reviewer
    appr.status = "REJECTED"
    appr.comments = req.comments or "Rejected by human reviewer."
    appr.reviewed_at = datetime.utcnow()
    
    proposal.status = "REJECTED"
    proposal.final_decision = "BLOCK"
    db.commit()

    return {
        "status": "REJECTED",
        "proposal_id": proposal.id,
        "message": f"Proposal rejected by {req.human_reviewer}. No funds disbursed."
    }
