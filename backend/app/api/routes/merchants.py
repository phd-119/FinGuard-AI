"""
FinGuard AI - Merchants API Routes
Provides merchant identity and global account state endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Merchant, FinancialState
from app.schemas.schemas import MerchantOut, MerchantCreate
from app.services.seed_data import seed_database

router = APIRouter(prefix="/merchants", tags=["Merchants"])

@router.get("", response_model=List[MerchantOut])
@router.get("/", response_model=List[MerchantOut])
def list_merchants(db: Session = Depends(get_db)):
    """
    List all active merchants in the FinGuard control plane sandbox.
    """
    merchants = db.query(Merchant).all()
    if not merchants:
        seed_database(db)
        merchants = db.query(Merchant).all()
        
    results = []
    for m in merchants:
        st = m.financial_state
        results.append(MerchantOut(
            id=m.id,
            name=m.name,
            business_category=m.business_category,
            created_at=m.created_at,
            cash_balance=st.cash_balance if st else 600000.0,
            reserve_requirement=st.reserve_requirement if st else 500000.0,
            available_balance=st.available_balance if st else 100000.0
        ))
    return results

@router.get("/{merchant_id}", response_model=MerchantOut)
def get_merchant(merchant_id: str, db: Session = Depends(get_db)):
    """
    Retrieve details for a specific merchant.
    """
    m = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not m:
        # Check if requested active default merchant
        m = db.query(Merchant).first()
        if not m:
            seed_database(db)
            m = db.query(Merchant).first()
            
    st = m.financial_state
    return MerchantOut(
        id=m.id,
        name=m.name,
        business_category=m.business_category,
        created_at=m.created_at,
        cash_balance=st.cash_balance if st else 600000.0,
        reserve_requirement=st.reserve_requirement if st else 500000.0,
        available_balance=st.available_balance if st else 100000.0
    )

@router.post("", response_model=MerchantOut)
@router.post("/", response_model=MerchantOut)
def create_merchant(payload: MerchantCreate, db: Session = Depends(get_db)):
    """
    Register a new merchant under FinGuard control plane governance.
    """
    m = Merchant(
        name=payload.name,
        business_category=payload.business_category
    )
    db.add(m)
    db.flush()
    
    st = FinancialState(
        merchant_id=m.id,
        cash_balance=payload.initial_cash,
        reserve_requirement=payload.reserve_requirement,
        available_balance=max(0.0, payload.initial_cash - payload.reserve_requirement),
        reserved_balance=payload.reserve_requirement
    )
    db.add(st)
    db.commit()
    db.refresh(m)
    
    return MerchantOut(
        id=m.id,
        name=m.name,
        business_category=m.business_category,
        created_at=m.created_at,
        cash_balance=st.cash_balance,
        reserve_requirement=st.reserve_requirement,
        available_balance=st.available_balance
    )
