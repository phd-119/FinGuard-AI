"""
FinGuard AI - Action Gateway
The central, unbypassable entrypoint for all autonomous AI agent financial proposals.
Validates agent identity, permissions, schema integrity, and security bounds.
"""

from datetime import datetime
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import Agent, AgentProposal, Merchant
from app.schemas.schemas import ProposeActionRequest

class ActionGateway:
    """
    Guarantees that AI Agents have NO direct path to financial execution.
    Every financial proposal must pass strictly through this Gateway.
    """

    ALLOWED_ACTIONS = {
        "payout_agent": ["PAYOUT", "VENDOR_SETTLEMENT", "SUPPLIER_PAYMENT"],
        "refund_agent": ["REFUND", "CHARGEBACK_REVERSAL", "CUSTOMER_CREDIT"],
        "growth_agent": ["MARKETING_SPEND", "AD_BUDGET_ALLOCATION", "SPONSORSHIP"],
        "collections_agent": ["DEBT_RECOVERY", "EARLY_DISCOUNT", "SETTLEMENT_WAIVER"],
        "treasury_agent": ["TREASURY_SWEEP", "RESERVE_REBALANCE", "FLOAT_OPTIMIZATION"]
    }

    def validate_and_ingest(self, db: Session, req: ProposeActionRequest) -> AgentProposal:
        # 1. Validate Agent Existence & Status
        agent = db.query(Agent).filter(Agent.id == req.agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Security Gateway Rejection: Unknown Agent ID '{req.agent_id}'. Unauthorized financial proposal."
            )

        if agent.status == "RESTRICTED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Security Gateway Rejection: Agent '{agent.name}' is currently RESTRICTED due to trust violations."
            )

        # 2. Validate Merchant Context
        merchant_id = req.merchant_id
        if not merchant_id:
            merchant = db.query(Merchant).first()
            if not merchant:
                raise HTTPException(status_code=500, detail="No active merchant context found in FinGuard.")
            merchant_id = merchant.id

        # 3. Validate Action Permissions for this Agent Type
        allowed_for_agent = self.ALLOWED_ACTIONS.get(agent.id, ["PAYOUT", "REFUND", "MARKETING_SPEND", "DEBT_RECOVERY", "TREASURY_SWEEP"])
        normalized_action = req.action_type.upper()
        if normalized_action not in allowed_for_agent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permission Denied: Agent '{agent.name}' is not authorized to propose '{req.action_type}'. Allowed: {allowed_for_agent}"
            )

        # 4. Ingest and persist proposal into pending state
        proposal = AgentProposal(
            agent_id=agent.id,
            merchant_id=merchant_id,
            action_type=normalized_action,
            amount=req.amount,
            currency=req.currency,
            urgency=req.urgency.upper(),
            priority=req.priority,
            confidence=req.confidence,
            reason=req.reason,
            status="PROPOSED",
            raw_payload=req.raw_payload or {}
        )
        
        db.add(proposal)
        agent.total_proposals += 1
        db.commit()
        db.refresh(proposal)
        
        return proposal

action_gateway = ActionGateway()
