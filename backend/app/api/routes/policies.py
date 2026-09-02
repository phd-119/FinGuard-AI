"""
FinGuard AI - Policies API Routes
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Policy
from app.schemas.schemas import PolicyOut

router = APIRouter(prefix="/policies", tags=["Policy Engine"])

@router.get("", response_model=List[PolicyOut])
def list_policies(db: Session = Depends(get_db)):
    """
    List all configured financial governance policies, limits, and reserve floors.
    """
    policies = db.query(Policy).all()
    return policies

@router.post("/{policy_id}/toggle", response_model=PolicyOut)
def toggle_policy(policy_id: str, db: Session = Depends(get_db)):
    """
    Enable or disable a specific governance policy.
    """
    pol = db.query(Policy).filter(Policy.id == policy_id).first()
    if not pol:
        raise HTTPException(status_code=404, detail=f"Policy '{policy_id}' not found.")
    pol.is_active = not pol.is_active
    db.commit()
    db.refresh(pol)
    return pol
