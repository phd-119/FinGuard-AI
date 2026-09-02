"""
FinGuard AI - Audit Trail & Receipts API Routes
Provides immutable cryptographic receipts and comprehensive audit logs answering:
"Why did FinGuard allow, modify, delay, escalate, or block this action?"
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import AuditRecord, TransactionLedger
from app.schemas.schemas import AuditReceiptOut

router = APIRouter(prefix="/audit", tags=["Audit Trail & Receipts"])

@router.get("", response_model=List[AuditReceiptOut])
def list_audit_records(
    agent_id: Optional[str] = None,
    decision: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all generated audit receipts across autonomous agents.
    """
    query = db.query(AuditRecord).order_by(AuditRecord.created_at.desc())
    if agent_id:
        query = query.filter(AuditRecord.agent_id == agent_id)
    if decision:
        query = query.filter(AuditRecord.governance_decision == decision)
        
    audits = query.all()
    return [
        AuditReceiptOut(
            receipt_number=a.receipt_number,
            action_hash=a.action_hash,
            proposal_id=a.proposal_id,
            agent_id=a.agent_id,
            agent_name=a.agent_name,
            original_amount=a.original_amount,
            approved_amount=a.approved_amount,
            governance_decision=a.governance_decision,
            risk_score=a.risk_score,
            conflict_detected=a.conflict_detected,
            conflict_summary=a.conflict_summary,
            human_approver=a.human_approver,
            execution_status=a.execution_status,
            decision_rationale=a.decision_rationale,
            timestamp=a.created_at,
            full_reasoning_payload=a.full_reasoning_payload or {}
        )
        for a in audits
    ]

@router.get("/{receipt_number}", response_model=AuditReceiptOut)
def get_audit_receipt(receipt_number: str, db: Session = Depends(get_db)):
    """
    Get a specific decision receipt by its receipt number.
    """
    a = db.query(AuditRecord).filter(AuditRecord.receipt_number == receipt_number).first()
    if not a:
        raise HTTPException(status_code=404, detail=f"Audit receipt '{receipt_number}' not found.")
    
    return AuditReceiptOut(
        receipt_number=a.receipt_number,
        action_hash=a.action_hash,
        proposal_id=a.proposal_id,
        agent_id=a.agent_id,
        agent_name=a.agent_name,
        original_amount=a.original_amount,
        approved_amount=a.approved_amount,
        governance_decision=a.governance_decision,
        risk_score=a.risk_score,
        conflict_detected=a.conflict_detected,
        conflict_summary=a.conflict_summary,
        human_approver=a.human_approver,
        execution_status=a.execution_status,
        decision_rationale=a.decision_rationale,
        timestamp=a.created_at,
        full_reasoning_payload=a.full_reasoning_payload or {}
    )

@router.get("/ledger/transactions", response_model=List[Dict[str, Any]])
def list_ledger_transactions(db: Session = Depends(get_db)):
    """
    Retrieve all transactions recorded in the simulated merchant ledger.
    """
    txs = db.query(TransactionLedger).order_by(TransactionLedger.timestamp.desc()).all()
    return [
        {
            "id": t.id,
            "merchant_id": t.merchant_id,
            "agent_id": t.agent_id,
            "proposal_id": t.proposal_id,
            "transaction_type": t.transaction_type,
            "amount": t.amount,
            "balance_after": t.balance_after,
            "description": t.description,
            "reference": t.reference,
            "timestamp": t.timestamp
        }
        for t in txs
    ]
