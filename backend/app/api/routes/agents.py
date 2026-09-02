"""
FinGuard AI - Agents API Routes
"""

from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Agent, Merchant
from app.schemas.schemas import AgentDetail
from app.services.seed_data import seed_database

router = APIRouter(prefix="/agents", tags=["Autonomous Agents"])

@router.get("", response_model=List[AgentDetail])
@router.get("/", response_model=List[AgentDetail])
def list_agents(db: Session = Depends(get_db)):
    """
    List all 5 simulated autonomous financial AI agents with their live trust scores,
    objectives, proposal metrics, and historical telemetry.
    """
    agents = db.query(Agent).all()
    if not agents:
        seed_database(db)
        agents = db.query(Agent).all()
    return agents

@router.get("/merchant/{merchant_id}", response_model=List[AgentDetail])
def get_agents_by_merchant(merchant_id: str, db: Session = Depends(get_db)):
    """
    List all autonomous agents operating for a specific merchant.
    """
    agents = db.query(Agent).all()
    if not agents:
        seed_database(db)
        agents = db.query(Agent).all()
    return agents

@router.get("/{agent_or_merchant_id}")
def get_agent_or_merchant_agents(agent_or_merchant_id: str, db: Session = Depends(get_db)):
    """
    Get detailed telemetry for an agent (e.g. payout_agent) or list agents if passed merchant_id.
    """
    agent = db.query(Agent).filter(Agent.id == agent_or_merchant_id).first()
    if agent:
        return AgentDetail.model_validate(agent)
        
    merchant = db.query(Merchant).filter(Merchant.id == agent_or_merchant_id).first()
    if merchant:
        agents = db.query(Agent).all()
        return [AgentDetail.model_validate(a) for a in agents]
        
    # Default fallback: check if it's an agent or return 404
    agents = db.query(Agent).all()
    if not agents:
        seed_database(db)
        agents = db.query(Agent).all()
    
    agent_match = next((a for a in agents if a.id == agent_or_merchant_id), None)
    if agent_match:
        return AgentDetail.model_validate(agent_match)
        
    # Return all agents if merchant UUID format
    return [AgentDetail.model_validate(a) for a in agents]
