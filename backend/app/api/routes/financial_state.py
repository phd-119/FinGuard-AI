"""
FinGuard AI - Financial State API Routes
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import FinancialState, Merchant, AgentProposal
from app.schemas.schemas import (
    FinancialStateOut, FinancialStateUpdate, PendingOutflowRequest, FinancialHealthOut
)
from app.services.seed_data import seed_database

router = APIRouter(prefix="/financial-state", tags=["Financial State Engine"])

@router.get("", response_model=FinancialStateOut)
@router.get("/", response_model=FinancialStateOut)
def get_default_financial_state(db: Session = Depends(get_db)):
    """
    Retrieve live merchant financial state: cash balance, reserve requirement,
    available balance, liquidity ratio, daily inflows/outflows, payables/receivables.
    """
    state = db.query(FinancialState).first()
    if not state:
        seed_database(db)
        state = db.query(FinancialState).first()
    return state

@router.get("/health", response_model=FinancialHealthOut)
def get_default_financial_health(db: Session = Depends(get_db)):
    """
    Returns liquidity runway, reserve status, and solvency health rating.
    """
    state = db.query(FinancialState).first()
    if not state:
        seed_database(db)
        state = db.query(FinancialState).first()
        
    free_liq = max(0.0, state.cash_balance - state.reserve_requirement)
    return FinancialHealthOut(
        merchant_id=state.merchant_id or "default_merchant",
        status="HEALTHY" if free_liq > 0 else "DEFICIT",
        cash_balance=state.cash_balance,
        reserve_requirement=state.reserve_requirement,
        free_liquidity=free_liq,
        liquidity_ratio=state.liquidity_ratio,
        runway_days=14 if state.daily_outflows == 0 else int(state.cash_balance / max(1.0, state.daily_outflows)),
        system_status="FIN_GUARD_PROTECTED"
    )

@router.get("/{merchant_id}/health", response_model=FinancialHealthOut)
def get_merchant_financial_health(merchant_id: str, db: Session = Depends(get_db)):
    """
    Returns liquidity runway and solvency health rating for a specific merchant.
    """
    state = db.query(FinancialState).filter(FinancialState.merchant_id == merchant_id).first()
    if not state:
        state = db.query(FinancialState).first()
        if not state:
            seed_database(db)
            state = db.query(FinancialState).first()
            
    free_liq = max(0.0, state.cash_balance - state.reserve_requirement)
    return FinancialHealthOut(
        merchant_id=merchant_id,
        status="HEALTHY" if free_liq > 0 else "DEFICIT",
        cash_balance=state.cash_balance,
        reserve_requirement=state.reserve_requirement,
        free_liquidity=free_liq,
        liquidity_ratio=state.liquidity_ratio,
        runway_days=14 if state.daily_outflows == 0 else int(state.cash_balance / max(1.0, state.daily_outflows)),
        system_status="FIN_GUARD_PROTECTED"
    )

@router.get("/{merchant_id}", response_model=FinancialStateOut)
def get_financial_state_by_merchant(merchant_id: str, db: Session = Depends(get_db)):
    """
    Retrieve live financial state for a specific merchant.
    """
    state = db.query(FinancialState).filter(FinancialState.merchant_id == merchant_id).first()
    if not state:
        state = db.query(FinancialState).first()
        if not state:
            seed_database(db)
            state = db.query(FinancialState).first()
    return state

@router.post("/reset", response_model=FinancialStateOut)
def reset_financial_state(db: Session = Depends(get_db)):
    """
    Resets the merchant financial state, agents, and ledger back to default sandbox values (₹6L cash, ₹5L reserve).
    """
    seed_database(db, force_reset=True)
    state = db.query(FinancialState).first()
    return state

@router.post("/{merchant_id}/add-pending-outflow", response_model=FinancialStateOut)
@router.post("/add-pending-outflow", response_model=FinancialStateOut)
def add_pending_outflow(payload: PendingOutflowRequest, merchant_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Records an active pending outflow from an agent proposal to update global concurrency state.
    """
    state = db.query(FinancialState).first()
    if not state:
        seed_database(db)
        state = db.query(FinancialState).first()
        
    if payload.action_type == "REFUND":
        state.pending_refunds += payload.amount
    else:
        state.pending_payouts += payload.amount
        
    db.commit()
    db.refresh(state)
    return state

@router.post("/{merchant_id}/remove-pending-outflow", response_model=FinancialStateOut)
@router.post("/remove-pending-outflow", response_model=FinancialStateOut)
def remove_pending_outflow(payload: PendingOutflowRequest, merchant_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Removes a cleared or executed pending outflow.
    """
    state = db.query(FinancialState).first()
    if not state:
        seed_database(db)
        state = db.query(FinancialState).first()
        
    if payload.action_type == "REFUND":
        state.pending_refunds = max(0.0, state.pending_refunds - payload.amount)
    else:
        state.pending_payouts = max(0.0, state.pending_payouts - payload.amount)
        
    db.commit()
    db.refresh(state)
    return state

@router.put("", response_model=FinancialStateOut)
@router.put("/{merchant_id}", response_model=FinancialStateOut)
def update_financial_state(payload: FinancialStateUpdate, merchant_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Adjust financial state parameters (e.g. inject cash, alter reserve floor) for sandbox testing.
    """
    state = db.query(FinancialState).first()
    if not state:
        raise HTTPException(status_code=404, detail="Financial state not initialized.")

    if payload.cash_balance is not None:
        state.cash_balance = payload.cash_balance
    if payload.reserve_requirement is not None:
        state.reserve_requirement = payload.reserve_requirement
    if payload.daily_inflows is not None:
        state.daily_inflows = payload.daily_inflows
    if payload.daily_outflows is not None:
        state.daily_outflows = payload.daily_outflows

    state.available_balance = max(0.0, state.cash_balance - state.reserve_requirement)
    state.liquidity_ratio = round(state.cash_balance / max(1.0, state.reserve_requirement), 3)

    db.commit()
    db.refresh(state)
    return state
