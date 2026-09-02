"""
FinGuard AI - Comprehensive End-to-End Live API Integration Test Suite
Validates all frontend-facing FastAPI routes strictly under the /api/v1 namespace.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.services.seed_data import seed_database

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    db = SessionLocal()
    seed_database(db, force_reset=True)
    db.close()

def test_system_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["control_plane"] == "FIN_GUARD_PROTECTED"

def test_merchants_api():
    # GET /api/v1/merchants
    res = client.get("/api/v1/merchants")
    assert res.status_code == 200
    merchants = res.json()
    assert len(merchants) >= 1
    m_id = merchants[0]["id"]

    # GET /api/v1/merchants/{merchant_id}
    res_m = client.get(f"/api/v1/merchants/{m_id}")
    assert res_m.status_code == 200
    assert res_m.json()["id"] == m_id

def test_agents_api():
    # GET /api/v1/agents
    res = client.get("/api/v1/agents")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) == 5

    # GET /api/v1/agents/payout_agent
    res_ag = client.get("/api/v1/agents/payout_agent")
    assert res_ag.status_code == 200
    assert res_ag.json()["id"] == "payout_agent"

def test_financial_state_api():
    # GET /api/v1/financial-state
    res = client.get("/api/v1/financial-state")
    assert res.status_code == 200
    assert res.json()["cash_balance"] == 600000.0
    assert res.json()["reserve_requirement"] == 500000.0

    # GET /api/v1/financial-state/health
    res_h = client.get("/api/v1/financial-state/health")
    assert res_h.status_code == 200
    assert res_h.json()["status"] == "HEALTHY"

    # POST /api/v1/financial-state/reset
    res_r = client.post("/api/v1/financial-state/reset")
    assert res_r.status_code == 200
    assert res_r.json()["cash_balance"] == 600000.0

def test_policies_api():
    # GET /api/v1/policies
    res = client.get("/api/v1/policies")
    assert res.status_code == 200
    policies = res.json()
    assert len(policies) >= 5

    # POST /api/v1/policies/{policy_id}/toggle
    pol_id = policies[0]["id"]
    res_tog = client.post(f"/api/v1/policies/{pol_id}/toggle")
    assert res_tog.status_code == 200
    assert res_tog.json()["is_active"] != policies[0]["is_active"]

def test_action_gateway_propose_and_reasoning():
    # POST /api/v1/actions/propose
    res_prop = client.post("/api/v1/actions/propose", json={
        "agent_id": "payout_agent",
        "action_type": "PAYOUT",
        "amount": 50000.0,
        "urgency": "LOW",
        "priority": 3,
        "confidence": 0.95,
        "reason": "Test standard vendor disbursement"
    })
    assert res_prop.status_code == 200
    data = res_prop.json()
    prop_id = data["proposal_id"]
    assert data["decision"]["decision"] == "ALLOW"

    # GET /api/v1/actions/status/{action_id}
    res_stat = client.get(f"/api/v1/actions/status/{prop_id}")
    assert res_stat.status_code == 200
    assert res_stat.json()["proposal_id"] == prop_id

    # GET /api/v1/actions/{action_id}
    res_act = client.get(f"/api/v1/actions/{prop_id}")
    assert res_act.status_code == 200

    # GET /api/v1/actions
    res_list = client.get("/api/v1/actions")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # GET /api/v1/simulations/{action_id}
    res_sim = client.get(f"/api/v1/simulations/{prop_id}")
    assert res_sim.status_code == 200
    assert len(res_sim.json()) == 4

def test_conflicts_and_risk_api():
    # GET /api/v1/conflicts
    res_c = client.get("/api/v1/conflicts")
    assert res_c.status_code == 200

    # GET /api/v1/risk
    res_r = client.get("/api/v1/risk")
    assert res_r.status_code == 200

def test_approvals_and_audit_api():
    # Propose high-risk action requiring approval
    res_prop = client.post("/api/v1/actions/propose", json={
        "agent_id": "payout_agent",
        "action_type": "PAYOUT",
        "amount": 400000.0,
        "urgency": "HIGH",
        "priority": 2,
        "confidence": 0.90,
        "reason": "Urgent high-value supplier payout"
    })
    prop_id = res_prop.json()["proposal_id"]

    # GET /api/v1/approvals
    res_appr = client.get("/api/v1/approvals")
    assert res_appr.status_code == 200
    apprs = res_appr.json()
    assert len(apprs) >= 1

    # POST /api/v1/approvals/{action_id}/approve
    res_sign = client.post(f"/api/v1/approvals/{prop_id}/approve", json={
        "human_reviewer": "Treasury Lead",
        "decision": "APPROVE",
        "approved_amount": 100000.0,
        "comments": "Approved split amount"
    })
    assert res_sign.status_code == 200

    # GET /api/v1/audit
    res_aud = client.get("/api/v1/audit")
    assert res_aud.status_code == 200
    receipts = res_aud.json()
    assert len(receipts) >= 1

    # GET /api/v1/audit/ledger/transactions
    res_tx = client.get("/api/v1/audit/ledger/transactions")
    assert res_tx.status_code == 200
    assert len(res_tx.json()) >= 1

def test_hero_demo_flow():
    # 1. Setup Hero Demo
    res_setup = client.post("/api/v1/demo/setup")
    assert res_setup.status_code == 200
    assert "COMPLETE" in res_setup.json()["status"] or res_setup.json()["status"] == "INITIALIZED"

    # 2. Run Hero Demo
    res_run = client.post("/api/v1/demo/run")
    assert res_run.status_code == 200
    data = res_run.json()
    assert data["decision"]["decision"] == "MODIFY"
    assert data["decision"]["modified_amount"] == 100000.0
    assert data["decision"]["deferred_amount"] == 300000.0

    # 3. Execute Hero Approval
    res_exec = client.post("/api/v1/demo/execute-hero")
    assert res_exec.status_code == 200
    assert res_exec.json()["updated_cash"] == 500000.0
    assert res_exec.json()["executed_amount"] == 100000.0
