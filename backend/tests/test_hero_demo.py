"""
FinGuard AI - Hero Demo End-to-End Test
Verifies the complete flagship demonstration scenario:
Cash: ₹6L | Reserve: ₹5L | Payout: ₹4L | Growth: ₹2L | Refund: ₹1L
Result: Global Conflict Detected -> Decision MODIFY (₹1L now + ₹3L deferred) -> Human Approval -> Safe Execution -> State Updated -> Audit Receipt Minted.
"""

from fastapi.testclient import TestClient
from app.main import app

def test_hero_demo_flow_end_to_end():
    client = TestClient(app)

    # 1. Trigger Hero Demo Run
    res_run = client.post("/api/v1/demo/run")
    assert res_run.status_code == 200
    data = res_run.json()

    # Verify FinGuard 10-Stage Pipeline Outputs
    assert data["agent_id"] == "payout_agent"
    assert data["original_amount"] == 400000.0
    assert data["intent"]["intent_label"] == "SUPPLIER_SETTLEMENT"
    
    # Verify Global Conflict Engine
    assert data["conflict"]["conflict_detected"] is True
    assert data["conflict"]["aggregate_outflow"] == 700000.0
    assert data["conflict"]["projected_shortfall"] == 600000.0
    assert len(data["conflict"]["detected_agents"]) == 3

    # Verify Future Impact Prediction
    assert data["future_impact"]["reserve_shortfall"] == 600000.0

    # Verify Risk & Decision
    assert data["decision"]["decision"] == "MODIFY"
    assert data["decision"]["modified_amount"] == 100000.0
    assert data["decision"]["deferred_amount"] == 300000.0
    assert data["decision"]["requires_human_approval"] is True

    # 2. Check Pending Approvals
    res_appr = client.get("/api/v1/approvals")
    assert res_appr.status_code == 200
    pending_list = res_appr.json()
    assert len(pending_list) >= 1
    target = next((p for p in pending_list if p["proposal_id"] == data["proposal_id"]), None)
    assert target is not None
    assert target["recommended_amount"] == 100000.0

    # 3. Simulate Human Approval and Execution
    proposal_id = data["proposal_id"]
    res_exec = client.post(f"/api/v1/approvals/{proposal_id}/approve", json={
        "human_reviewer": "Lead Treasury Officer",
        "decision": "APPROVE",
        "approved_amount": 100000.0,
        "comments": "Approved modified amount of ₹1L to honor urgent supplier payment while preserving statutory reserve."
    })
    assert res_exec.status_code == 200
    exec_data = res_exec.json()
    assert exec_data["status"] == "EXECUTED"
    assert exec_data["executed_amount"] == 100000.0
    assert exec_data["post_execution_cash"] == 500000.0
    assert exec_data["post_execution_reserve"] == 500000.0

    # 4. Verify Financial State is safely preserved
    res_state = client.get("/api/v1/financial-state")
    assert res_state.status_code == 200
    state_data = res_state.json()
    assert state_data["cash_balance"] == 500000.0
    assert state_data["reserve_requirement"] == 500000.0

    # 5. Verify Cryptographic Audit Receipt Generation
    res_audit = client.get("/api/v1/audit")
    assert res_audit.status_code == 200
    audits = res_audit.json()
    assert len(audits) >= 1
    latest_receipt = audits[0]
    assert latest_receipt["receipt_number"].startswith("FG-RCPT-")
    assert latest_receipt["approved_amount"] == 100000.0
    assert latest_receipt["conflict_detected"] is True
    assert latest_receipt["execution_status"] == "EXECUTED"
