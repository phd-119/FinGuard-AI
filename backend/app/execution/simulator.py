"""
FinGuard AI - Financial Execution Simulator & Ledger
Safe simulated financial execution layer and tamper-evident audit record generator.
(NO real money movement - 100% simulated sandbox).
"""

import hashlib
import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import (
    AgentProposal, FinancialState, ExecutionRecord, AuditRecord, TransactionLedger, Agent
)
from app.schemas.schemas import ExecutionResultOut, AuditReceiptOut

class ExecutionSimulator:
    def execute_governed_action(
        self,
        db: Session,
        proposal: AgentProposal,
        approved_amount: float,
        human_approver: str = "FinGuard Autonomous Control Plane",
        approval_comment: str = "Execution verified against governance policy and reserve constraints."
    ) -> ExecutionResultOut:
        
        # 1. State check
        state = db.query(FinancialState).filter(FinancialState.merchant_id == proposal.merchant_id).first()
        if not state:
            raise HTTPException(status_code=500, detail="Financial state not found for merchant.")

        pre_cash = state.cash_balance
        pre_reserve = state.reserved_balance

        # 2. Check sufficient balance
        if pre_cash < approved_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Execution Failed: Insufficient cash balance (₹{pre_cash:,.2f}) for execution of ₹{approved_amount:,.2f}"
            )

        # 3. Simulate balance deductions and state updates
        post_cash = pre_cash - approved_amount
        state.cash_balance = round(post_cash, 2)
        state.daily_outflows = round(state.daily_outflows + approved_amount, 2)
        state.available_balance = max(0.0, round(post_cash - state.reserve_requirement, 2))
        state.liquidity_ratio = round(post_cash / max(1.0, state.reserve_requirement), 3)

        if proposal.action_type in ["PAYOUT", "VENDOR_SETTLEMENT"]:
            state.payables = max(0.0, state.payables - approved_amount)
        elif proposal.action_type in ["REFUND", "CHARGEBACK_REVERSAL"]:
            state.pending_refunds = max(0.0, state.pending_refunds - approved_amount)
        elif proposal.action_type in ["MARKETING_SPEND", "AD_BUDGET_ALLOCATION"]:
            state.marketing_spend = round(state.marketing_spend + approved_amount, 2)

        tx_ref = f"SIM-TXN-{uuid.uuid4().hex[:10].upper()}"

        # 4. Create Execution Record
        execution = ExecutionRecord(
            proposal_id=proposal.id,
            status="EXECUTED",
            executed_amount=approved_amount,
            transaction_reference=tx_ref,
            pre_execution_cash=pre_cash,
            post_execution_cash=post_cash,
            pre_execution_reserve=pre_reserve,
            post_execution_reserve=state.reserved_balance,
            metadata_json={
                "merchant_id": proposal.merchant_id,
                "agent_id": proposal.agent_id,
                "action_type": proposal.action_type,
                "governance_decision": proposal.final_decision
            }
        )
        db.add(execution)

        # 5. Append to Transaction Ledger
        agent = db.query(Agent).filter(Agent.id == proposal.agent_id).first()
        agent_name = agent.name if agent else proposal.agent_id
        
        ledger_entry = TransactionLedger(
            merchant_id=proposal.merchant_id,
            agent_id=proposal.agent_id,
            proposal_id=proposal.id,
            transaction_type=proposal.action_type,
            amount=approved_amount,
            balance_after=post_cash,
            description=f"Governed execution of {proposal.action_type} proposed by {agent_name}: {proposal.reason[:80]}",
            reference=tx_ref
        )
        db.add(ledger_entry)

        # 6. Generate Cryptographic Audit Receipt
        receipt_num = f"FG-RCPT-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        hash_payload = f"{proposal.id}:{proposal.agent_id}:{approved_amount}:{tx_ref}:{post_cash}"
        action_hash = hashlib.sha256(hash_payload.encode()).hexdigest()

        # Extract reasoning payload from relationships or proposal
        reasoning_payload = {
            "proposal_id": proposal.id,
            "agent_id": proposal.agent_id,
            "agent_name": agent_name,
            "original_amount": proposal.amount,
            "executed_amount": approved_amount,
            "intent_label": proposal.intent_label,
            "decision": proposal.final_decision,
            "pre_cash": pre_cash,
            "post_cash": post_cash,
            "reserve_requirement": state.reserve_requirement,
            "human_approver": human_approver,
            "approval_comment": approval_comment,
            "timestamp": datetime.utcnow().isoformat()
        }

        audit = AuditRecord(
            proposal_id=proposal.id,
            receipt_number=receipt_num,
            action_hash=action_hash,
            agent_id=proposal.agent_id,
            agent_name=agent_name,
            original_amount=proposal.amount,
            approved_amount=approved_amount,
            governance_decision=proposal.final_decision or "ALLOW",
            risk_score=proposal.risk_assessment.risk_score if proposal.risk_assessment else 25.0,
            conflict_detected=proposal.conflict.conflict_detected if proposal.conflict else False,
            conflict_summary=proposal.conflict.explanation if proposal.conflict else None,
            human_approver=human_approver,
            execution_status="EXECUTED",
            decision_rationale=proposal.decision_record.decision_reason if proposal.decision_record else "Standard approval",
            full_reasoning_payload=reasoning_payload
        )
        db.add(audit)

        # 7. Update Proposal Status
        proposal.status = "EXECUTED"
        db.commit()
        db.refresh(execution)

        return ExecutionResultOut(
            execution_id=execution.id,
            proposal_id=proposal.id,
            status="EXECUTED",
            executed_amount=approved_amount,
            transaction_reference=tx_ref,
            pre_execution_cash=pre_cash,
            post_execution_cash=post_cash,
            pre_execution_reserve=pre_reserve,
            post_execution_reserve=state.reserved_balance,
            executed_at=execution.executed_at,
            message=f"Financial action successfully simulated. Cash updated from ₹{pre_cash:,.2f} to ₹{post_cash:,.2f}. Audit Receipt: {receipt_num}"
        )

execution_simulator = ExecutionSimulator()
