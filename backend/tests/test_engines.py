"""
FinGuard AI - Unit Tests for Specialized Governance Engines
"""

import pytest
from app.models.models import Merchant, FinancialState, Agent, AgentProposal, Policy
from app.schemas.schemas import ProposeActionRequest
from app.engines.action_gateway import action_gateway
from app.engines.intent_engine import intent_engine
from app.engines.policy_engine import policy_engine
from app.engines.conflict_engine import conflict_engine
from app.engines.prediction_engine import prediction_engine
from app.engines.trust_engine import trust_engine
from app.engines.simulation_engine import simulation_engine
from app.engines.optimization_engine import optimization_engine
from app.engines.alternative_engine import alternative_engine
from app.engines.decision_engine import decision_engine

def test_action_gateway_validation(db_session):
    # Valid proposal
    req = ProposeActionRequest(
        agent_id="payout_agent",
        action_type="PAYOUT",
        amount=50000.0,
        urgency="LOW",
        reason="Vendor invoice clearing for warehouse equipment"
    )
    prop = action_gateway.validate_and_ingest(db_session, req)
    assert prop.id is not None
    assert prop.amount == 50000.0
    assert prop.status == "PROPOSED"

def test_intent_engine(db_session):
    agent = db_session.query(Agent).filter(Agent.id == "refund_agent").first()
    prop = AgentProposal(
        agent_id="refund_agent",
        merchant_id=db_session.query(Merchant).first().id,
        action_type="REFUND",
        amount=1500.0,
        urgency="HIGH",
        reason="Customer dispute and chargeback return for damaged item"
    )
    res = intent_engine.evaluate(prop, agent)
    assert res.intent_label == "CUSTOMER_REFUND"
    assert res.financial_effect == "IMMEDIATE_CASH_OUTFLOW"

def test_policy_engine_reserve_compliance(db_session):
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 600000.0
    state.reserve_requirement = 500000.0
    db_session.commit()
    agent = db_session.query(Agent).filter(Agent.id == "payout_agent").first()

    # Proposal within reserve buffer (₹50k from ₹100k free cash)
    prop_ok = AgentProposal(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=50000.0,
        urgency="LOW",
        reason="Routine vendor payment"
    )
    checks_ok = policy_engine.evaluate(db_session, prop_ok, state, agent)
    reserve_check = next(c for c in checks_ok if c.policy_code == "POL_RESERVE_FLOOR")
    assert reserve_check.is_compliant is True

    # Proposal breaching reserve buffer (₹400k from ₹100k free cash)
    prop_breach = AgentProposal(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=400000.0,
        urgency="HIGH",
        reason="Large supplier payout"
    )
    checks_breach = policy_engine.evaluate(db_session, prop_breach, state, agent)
    reserve_check_b = next(c for c in checks_breach if c.policy_code == "POL_RESERVE_FLOOR")
    assert reserve_check_b.is_compliant is False

def test_conflict_engine_detection(db_session):
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 600000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    # Clear pending
    db_session.query(AgentProposal).filter(AgentProposal.status == "PROPOSED").delete()
    db_session.commit()

    # Add Growth Agent proposal (₹2L) and Refund Agent proposal (₹1L)
    p_growth = AgentProposal(
        agent_id="growth_agent",
        merchant_id=merchant.id,
        action_type="MARKETING_SPEND",
        amount=200000.0,
        urgency="MEDIUM",
        reason="Marketing campaign",
        status="PROPOSED"
    )
    p_refund = AgentProposal(
        agent_id="refund_agent",
        merchant_id=merchant.id,
        action_type="REFUND",
        amount=100000.0,
        urgency="HIGH",
        reason="Refund batch",
        status="PROPOSED"
    )
    db_session.add_all([p_growth, p_refund])
    db_session.commit()

    # Now evaluate Payout Agent proposal (₹4L)
    p_payout = AgentProposal(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=400000.0,
        urgency="HIGH",
        reason="Supplier invoice",
        status="PROPOSED"
    )
    db_session.add(p_payout)
    db_session.commit()

    conflict_res = conflict_engine.detect_conflicts(db_session, p_payout, state)
    assert conflict_res.conflict_detected is True
    assert conflict_res.aggregate_outflow == 700000.0
    assert conflict_res.projected_shortfall == 600000.0
    assert conflict_res.severity in ["HIGH", "CRITICAL"]

def test_optimization_engine_split_and_multi_agent(db_session):
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 600000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    prop = AgentProposal(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=400000.0,
        urgency="HIGH",
        reason="Supplier payout",
        status="PROPOSED"
    )

    imm, deferred, delay = optimization_engine.optimize_split_allocation(prop, state)
    assert imm == 100000.0
    assert deferred == 300000.0
    assert delay == 24

    # Multi-agent allocation test
    proposals_list = [
        {"agent": "Refund Agent", "amount": 50000.0, "urgency": "CRITICAL", "priority": 1, "trust_score": 95.0},
        {"agent": "Payout Agent", "amount": 80000.0, "urgency": "HIGH", "priority": 2, "trust_score": 90.0},
        {"agent": "Growth Agent", "amount": 100000.0, "urgency": "LOW", "priority": 4, "trust_score": 80.0}
    ]
    # Free cash = 100,000 (600,000 - 500,000)
    alloc_results = optimization_engine.optimize_multi_agent_allocations(
        proposals=proposals_list,
        available_cash=600000.0,
        reserve_requirement=500000.0
    )
    assert len(alloc_results) == 3
    # Refund Agent gets full 50,000
    assert alloc_results[0]["allocated_immediate"] == 50000.0
    # Payout Agent gets remaining 50,000 (partial of 80,000)
    assert alloc_results[1]["allocated_immediate"] == 50000.0
    assert alloc_results[1]["deferred_amount"] == 30000.0
    # Growth Agent is deferred
    assert alloc_results[2]["allocated_immediate"] == 0.0

def test_simulation_and_alternative_engine(db_session):
    merchant = db_session.query(Merchant).first()
    state = db_session.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    state.cash_balance = 600000.0
    state.reserve_requirement = 500000.0
    db_session.commit()

    prop = AgentProposal(
        agent_id="payout_agent",
        merchant_id=merchant.id,
        action_type="PAYOUT",
        amount=400000.0,
        urgency="HIGH",
        reason="Supplier payout",
        status="PROPOSED"
    )
    
    from app.schemas.schemas import ConflictDetectionResult
    dummy_conflict = ConflictDetectionResult(
        conflict_detected=True,
        conflict_type="GLOBAL_LIQUIDITY_RESERVE_BREACH",
        severity="HIGH",
        detected_agents=[],
        aggregate_outflow=700000.0,
        available_cash=600000.0,
        required_reserve=500000.0,
        projected_shortfall=600000.0,
        explanation="Test conflict"
    )

    scenarios = simulation_engine.simulate_scenarios(prop, state, dummy_conflict)
    assert len(scenarios) == 4
    
    rec_sc = next(s for s in scenarios if s.is_recommended)
    assert rec_sc.scenario_id == "SCENARIO_B"
    assert rec_sc.immediate_outflow == 100000.0
    assert rec_sc.deferred_outflow == 300000.0

    alt = alternative_engine.generate_alternative(prop, state, rec_sc)
    assert alt.alternative_type == "SPLIT_TRANSACTION"
    assert alt.immediate_amount == 100000.0
    assert alt.deferred_amount == 300000.0
