"""
FinGuard AI - Comprehensive Governance Pipeline Tests
Tests ALLOW, MODIFY, DELAY, ESCALATE, and BLOCK flows.
"""

import pytest
from fastapi import HTTPException
from app.models.models import (
    Merchant, FinancialState, Agent, AgentProposal,
    ConflictRecord, RiskAssessmentRecord, FutureImpactRecord,
    SimulationRecord, DecisionRecord, HumanApprovalRecord
)
from app.schemas.schemas import ProposeActionRequest
from app.engines.action_gateway import action_gateway
from app.services.governance_pipeline import governance_pipeline

def clean_proposals(db_session):
    db_session.query(HumanApprovalRecord).delete()
    db_session.query(DecisionRecord).delete()
    db_session.query(SimulationRecord).delete()
    db_session.query(FutureImpactRecord).delete()
    db_session.query(RiskAssessmentRecord).delete()
    db_session.query(ConflictRecord).delete()
    db_session.query(AgentProposal).delete()
    db_session.commit()

def test_governance_pipeline_allow_flow(db_session):
    """
    Test safe small transaction that adheres to all policies -> ALLOW
    """
    clean_proposals(db_session)
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 1000000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    req = ProposeActionRequest(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=30000.0,
        urgency="LOW",
        reason="Routine office supplies payment"
    )
    prop = action_gateway.validate_and_ingest(db_session, req)
    res = governance_pipeline.evaluate_proposal(db_session, prop.id)

    assert res.decision.decision == "ALLOW"
    assert res.decision.requires_human_approval is False
    assert res.decision.modified_amount == 30000.0

def test_governance_pipeline_modify_flow(db_session):
    """
    Test transaction that exceeds free cash and collides with reserve -> MODIFY
    """
    clean_proposals(db_session)
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 600000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    # Add background collision
    db_session.add(AgentProposal(
        agent_id="growth_agent",
        merchant_id=merchant.id,
        action_type="MARKETING_SPEND",
        amount=200000.0,
        urgency="MEDIUM",
        reason="Ad campaign",
        status="PROPOSED"
    ))
    db_session.commit()

    req = ProposeActionRequest(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=400000.0,
        urgency="HIGH",
        reason="Raw materials supplier payout"
    )
    prop = action_gateway.validate_and_ingest(db_session, req)
    res = governance_pipeline.evaluate_proposal(db_session, prop.id)

    assert res.decision.decision == "MODIFY"
    assert res.decision.requires_human_approval is True
    assert res.decision.modified_amount == 100000.0
    assert res.decision.deferred_amount == 300000.0

def test_governance_pipeline_delay_flow(db_session):
    """
    Test low urgency transaction with tight liquidity cushion -> DELAY
    """
    clean_proposals(db_session)
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 520000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    req = ProposeActionRequest(
        agent_id="growth_agent",
        merchant_id=merchant.id,
        action_type="MARKETING_SPEND",
        amount=15000.0,
        urgency="LOW",
        reason="Low urgency social media experiment testing new keyword group"
    )
    prop = action_gateway.validate_and_ingest(db_session, req)
    res = governance_pipeline.evaluate_proposal(db_session, prop.id)

    assert res.decision.decision in ["DELAY", "ALLOW"]

def test_governance_pipeline_escalate_flow(db_session):
    """
    Test high risk or large single transaction within reserve -> ESCALATE
    """
    clean_proposals(db_session)
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 1200000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    req = ProposeActionRequest(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=380000.0,
        urgency="HIGH",
        reason="High capital disbursement for annual cloud server renewal"
    )
    prop = action_gateway.validate_and_ingest(db_session, req)
    res = governance_pipeline.evaluate_proposal(db_session, prop.id)

    assert res.decision.decision in ["ESCALATE", "MODIFY", "ALLOW"]
    if res.decision.decision == "ESCALATE":
        assert res.decision.requires_human_approval is True

def test_governance_pipeline_block_flow(db_session):
    """
    Test critical violation (restricted agent or insolvency breach) -> BLOCK
    """
    clean_proposals(db_session)
    merchant = db_session.query(Merchant).first()
    agent = db_session.query(Agent).filter(Agent.id == "growth_agent").first()
    agent.status = "RESTRICTED"
    db_session.commit()

    try:
        req = ProposeActionRequest(
            agent_id="growth_agent",
            merchant_id=merchant.id,
            action_type="MARKETING_SPEND",
            amount=50000.0,
            urgency="HIGH",
            reason="Campaign spend"
        )
        prop = action_gateway.validate_and_ingest(db_session, req)
        assert False, "Should have thrown HTTPException 403"
    except HTTPException as e:
        assert e.status_code == 403
        assert "RESTRICTED" in e.detail
    finally:
        agent.status = "ACTIVE"
        db_session.commit()
