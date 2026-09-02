"""
FinGuard AI - Hero Demo API Routes
Reproducible scenario showcasing Global Multi-Agent Financial Governance:
Cash: ₹6,00,000 | Required Reserve: ₹5,00,000
Payout Agent (₹4L) + Growth Agent (₹2L) + Refund Agent (₹1L) = ₹7L Outflow -> MODIFY Decision (₹1L now + ₹3L later).
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Merchant, FinancialState, AgentProposal, Agent
from app.schemas.schemas import EvaluationPipelineResponse, ProposeActionRequest
from app.services.seed_data import seed_database
from app.engines.action_gateway import action_gateway
from app.services.governance_pipeline import governance_pipeline
from app.execution.simulator import execution_simulator

router = APIRouter(prefix="/demo", tags=["Hero Scenario Demo"])

@router.post("/setup", response_model=Dict[str, Any])
def setup_hero_demo(db: Session = Depends(get_db)):
    """
    Step 1 of Hero Demo:
    Initializes Merchant Cash at ₹6,00,000 and Reserve Requirement at ₹5,00,000.
    Pre-populates concurrent proposals from Growth Agent (₹2,00,000) and Refund Agent (₹1,00,000).
    """
    seed_database(db, force_reset=True)
    
    merchant = db.query(Merchant).first()
    state = db.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    
    # Ensure baseline hero numbers
    state.cash_balance = 600000.0
    state.reserve_requirement = 500000.0
    state.available_balance = 100000.0
    state.reserved_balance = 500000.0
    state.liquidity_ratio = 1.20
    db.commit()

    # 1. Growth Agent proposes ₹2,00,000
    prop_growth = action_gateway.validate_and_ingest(
        db=db,
        req=ProposeActionRequest(
            agent_id="growth_agent",
            merchant_id=merchant.id,
            action_type="MARKETING_SPEND",
            amount=200000.0,
            currency="INR",
            urgency="MEDIUM",
            priority=3,
            confidence=0.91,
            reason="Q4 Omnichannel Festive Marketing Blitz allocation across search & social channels.",
            raw_payload={"campaign_id": "FESTIVE-Q4", "target_channels": ["Google", "Meta"]}
        )
    )

    # 2. Refund Agent proposes ₹1,00,000
    prop_refund = action_gateway.validate_and_ingest(
        db=db,
        req=ProposeActionRequest(
            agent_id="refund_agent",
            merchant_id=merchant.id,
            action_type="REFUND",
            amount=100000.0,
            currency="INR",
            urgency="HIGH",
            priority=2,
            confidence=0.98,
            reason="Bulk customer refund settlement for defective electronics batch #8820.",
            raw_payload={"batch_id": "BATCH-8820", "orders_count": 48}
        )
    )

    return {
        "status": "HERO_DEMO_SETUP_COMPLETE",
        "merchant_name": merchant.name,
        "cash_balance": state.cash_balance,
        "reserve_requirement": state.reserve_requirement,
        "free_cash": state.available_balance,
        "concurrent_proposals": [
            {"agent": "Growth Agent", "amount": 200000.0, "proposal_id": prop_growth.id},
            {"agent": "Refund Agent", "amount": 100000.0, "proposal_id": prop_refund.id}
        ],
        "message": "Hero state initialized. Ready for Payout Agent proposal of ₹4,00,000."
    }

@router.post("/run", response_model=EvaluationPipelineResponse)
def run_hero_demo(db: Session = Depends(get_db)):
    """
    Runs the complete Hero Demo in a single click:
    1. Sets up Cash ₹6L and Reserve ₹5L with Growth (₹2L) and Refund (₹1L) active.
    2. Payout Agent submits ₹4,00,000 payout proposal.
    3. Action Gateway intercepts and routes through FinGuard 10-Stage Pipeline.
    4. Detects global conflict (₹7L total outflow vs ₹6L cash).
    5. Simulates scenarios & computes safe modification (₹1L immediate + ₹3L delayed).
    6. Produces governed decision: MODIFY.
    """
    setup_hero_demo(db)
    
    merchant = db.query(Merchant).first()

    # Payout Agent proposes ₹4,00,000
    payout_req = ProposeActionRequest(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=400000.0,
        currency="INR",
        urgency="HIGH",
        priority=1,
        confidence=0.94,
        reason="Settlement of raw material invoice #INV-9902 for critical primary manufacturing supplier.",
        raw_payload={"vendor_id": "SUPPLIER-ALPHA-99", "invoice_num": "INV-9902", "terms": "NET-15"}
    )

    proposal = action_gateway.validate_and_ingest(db, payout_req)
    result = governance_pipeline.evaluate_proposal(db, proposal.id)
    return result

@router.post("/execute-hero", response_model=Dict[str, Any])
def execute_hero_approval(db: Session = Depends(get_db)):
    """
    Simulates Treasury Lead approving the governed MODIFY decision (₹1,00,000 immediate).
    Executes the action, updates state to ₹5,00,000 cash (Reserve 100% Intact), and produces receipt.
    """
    payout_proposal = db.query(AgentProposal).filter(
        AgentProposal.agent_id == "payout_agent",
        AgentProposal.status.in_(["AWAITING_APPROVAL", "DECIDED", "PROPOSED"])
    ).order_by(AgentProposal.created_at.desc()).first()

    if not payout_proposal:
        return {"error": "No pending hero payout proposal found. Run /demo/run first."}

    exec_result = execution_simulator.execute_governed_action(
        db=db,
        proposal=payout_proposal,
        approved_amount=100000.0, # The governed modified amount
        human_approver="Treasury Lead (Internship Pitch Reviewer)",
        approval_comment="Approved FinGuard Governed Modification: Disbursing ₹1,00,000 now, ₹3,00,000 deferred."
    )

    state = db.query(FinancialState).filter(FinancialState.merchant_id == payout_proposal.merchant_id).first()

    return {
        "status": "HERO_EXECUTION_COMPLETE",
        "proposal_id": payout_proposal.id,
        "original_amount": 400000.0,
        "executed_amount": 100000.0,
        "deferred_amount": 300000.0,
        "updated_cash": state.cash_balance,
        "reserve_requirement": state.reserve_requirement,
        "reserve_status": "100% PROTECTED",
        "transaction_reference": exec_result.transaction_reference,
        "execution_message": exec_result.message
    }
