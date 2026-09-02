"""
FinGuard AI - General API Endpoints Test Suite
Tests API routing strictly under /api/v1 namespace.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_and_root():
    res_h = client.get("/health")
    assert res_h.status_code == 200
    assert res_h.json()["control_plane"] == "FIN_GUARD_PROTECTED"

    res_r = client.get("/")
    assert res_r.status_code == 200
    assert res_r.json()["project"] == "FinGuard AI"

def test_merchants_endpoints():
    res = client.get("/api/v1/merchants")
    assert res.status_code == 200
    merchants = res.json()
    assert len(merchants) >= 1
    assert "cash_balance" in merchants[0]

def test_agents_endpoints():
    res = client.get("/api/v1/agents")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) == 5
    ids = [a["id"] for a in agents]
    assert "payout_agent" in ids
    assert "refund_agent" in ids
    assert "growth_agent" in ids
    assert "collections_agent" in ids
    assert "treasury_agent" in ids

def test_financial_state_and_health_endpoints():
    res = client.get("/api/v1/financial-state")
    assert res.status_code == 200
    data = res.json()
    assert "cash_balance" in data
    assert "reserve_requirement" in data

    res_h = client.get("/api/v1/financial-state/health")
    assert res_h.status_code == 200
    assert res_h.json()["system_status"] == "FIN_GUARD_PROTECTED"

def test_policies_endpoints():
    res = client.get("/api/v1/policies")
    assert res.status_code == 200
    policies = res.json()
    assert len(policies) >= 5

def test_action_gateway_rejects_unauthorized_agent():
    res = client.post("/api/v1/actions/propose", json={
        "agent_id": "malicious_unregistered_agent",
        "action_type": "PAYOUT",
        "amount": 1000000.0,
        "reason": "Unauthorized drain"
    })
    assert res.status_code == 404
