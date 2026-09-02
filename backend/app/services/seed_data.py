"""
FinGuard AI - Database Seeder & State Reset Service
Initializes realistic synthetic merchant state, 5 autonomous AI agents, policies, and ledger.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import (
    Merchant, FinancialState, Agent, Policy, AgentProposal,
    TransactionLedger, ConflictRecord, RiskAssessmentRecord,
    FutureImpactRecord, SimulationRecord, DecisionRecord, ExecutionRecord, AuditRecord
)

def seed_database(db: Session, force_reset: bool = False):
    if force_reset:
        db.query(AuditRecord).delete()
        db.query(ExecutionRecord).delete()
        db.query(DecisionRecord).delete()
        db.query(SimulationRecord).delete()
        db.query(FutureImpactRecord).delete()
        db.query(RiskAssessmentRecord).delete()
        db.query(ConflictRecord).delete()
        db.query(TransactionLedger).delete()
        db.query(AgentProposal).delete()
        db.query(Policy).delete()
        db.query(Agent).delete()
        db.query(FinancialState).delete()
        db.query(Merchant).delete()
        db.commit()

    # 1. Merchant
    merchant = db.query(Merchant).first()
    if not merchant:
        merchant = Merchant(
            name="OmniRetail D2C India",
            business_category="E-Commerce / Direct-to-Consumer"
        )
        db.add(merchant)
        db.commit()
        db.refresh(merchant)

    # 2. Financial State
    state = db.query(FinancialState).filter(FinancialState.merchant_id == merchant.id).first()
    if not state:
        state = FinancialState(
            merchant_id=merchant.id,
            cash_balance=600000.0,         # ₹6,00,000 available cash
            available_balance=100000.0,    # ₹1,00,000 free cash
            reserved_balance=500000.0,     # ₹5,00,000 locked reserve
            reserve_requirement=500000.0,  # ₹5,00,000 required reserve
            daily_inflows=120000.0,
            daily_outflows=45000.0,
            pending_payouts=0.0,
            pending_refunds=0.0,
            receivables=350000.0,
            payables=480000.0,
            marketing_spend=85000.0,
            liquidity_ratio=1.20
        )
        db.add(state)
        db.commit()

    # 3. 5 Autonomous AI Agents
    agents_data = [
        {
            "id": "payout_agent",
            "name": "Payout Agent",
            "agent_type": "PAYOUT_OPTIMIZER",
            "objective": "Optimize supplier/vendor payouts while maintaining liquidity and honoring credit terms.",
            "trust_score": 88.5,
            "trust_level": "HIGH",
            "status": "ACTIVE",
            "total_proposals": 42,
            "approved_proposals": 36,
            "modified_proposals": 5,
            "blocked_proposals": 1,
            "violation_count": 0,
            "historical_telemetry": [
                {"timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(), "action": "Vendor Settlement #401", "amount": 150000.0, "decision": "ALLOW"},
                {"timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat(), "action": "Supplier Batch #398", "amount": 320000.0, "decision": "MODIFY"}
            ]
        },
        {
            "id": "refund_agent",
            "name": "Refund Agent",
            "agent_type": "REFUND_CONTROLLER",
            "objective": "Process customer refunds, disputed chargebacks, and returns while respecting refund policies.",
            "trust_score": 94.0,
            "trust_level": "VERIFIED",
            "status": "ACTIVE",
            "total_proposals": 78,
            "approved_proposals": 76,
            "modified_proposals": 2,
            "blocked_proposals": 0,
            "violation_count": 0,
            "historical_telemetry": [
                {"timestamp": (datetime.utcnow() - timedelta(hours=18)).isoformat(), "action": "Damaged Shipment Refund #1024", "amount": 4200.0, "decision": "ALLOW"},
                {"timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(), "action": "Bulk Order Return Batch", "amount": 45000.0, "decision": "ALLOW"}
            ]
        },
        {
            "id": "growth_agent",
            "name": "Growth Agent",
            "agent_type": "MARKETING_ALLOCATOR",
            "objective": "Allocate dynamic capital toward high-ROI performance marketing and customer acquisition campaigns.",
            "trust_score": 82.0,
            "trust_level": "MEDIUM",
            "status": "ACTIVE",
            "total_proposals": 29,
            "approved_proposals": 22,
            "modified_proposals": 6,
            "blocked_proposals": 1,
            "violation_count": 1,
            "historical_telemetry": [
                {"timestamp": (datetime.utcnow() - timedelta(days=3)).isoformat(), "action": "Google Ads Sprint Top-up", "amount": 100000.0, "decision": "ALLOW"},
                {"timestamp": (datetime.utcnow() - timedelta(days=7)).isoformat(), "action": "Influencer Blitz Deposit", "amount": 250000.0, "decision": "MODIFY"}
            ]
        },
        {
            "id": "collections_agent",
            "name": "Collections Agent",
            "agent_type": "RECEIVABLES_RECOVERY",
            "objective": "Accelerate incoming cash collections and execute automated recovery workflows for overdue receivables.",
            "trust_score": 91.0,
            "trust_level": "HIGH",
            "status": "ACTIVE",
            "total_proposals": 35,
            "approved_proposals": 34,
            "modified_proposals": 1,
            "blocked_proposals": 0,
            "violation_count": 0,
            "historical_telemetry": [
                {"timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(), "action": "Early Settlement Incentive 2%", "amount": 12000.0, "decision": "ALLOW"},
                {"timestamp": (datetime.utcnow() - timedelta(days=4)).isoformat(), "action": "Delinquent Account Recovery Discount", "amount": 8500.0, "decision": "ALLOW"}
            ]
        },
        {
            "id": "treasury_agent",
            "name": "Treasury Agent",
            "agent_type": "LIQUIDITY_BUFFER_MANAGER",
            "objective": "Maintain liquidity buffers, optimize float yields, and enforce statutory reserve compliance.",
            "trust_score": 96.5,
            "trust_level": "VERIFIED",
            "status": "ACTIVE",
            "total_proposals": 60,
            "approved_proposals": 59,
            "modified_proposals": 1,
            "blocked_proposals": 0,
            "violation_count": 0,
            "historical_telemetry": [
                {"timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(), "action": "Overnight Float Sweep to Liquid Fund", "amount": 200000.0, "decision": "ALLOW"},
                {"timestamp": (datetime.utcnow() - timedelta(days=6)).isoformat(), "action": "Reserve Rebalancing", "amount": 100000.0, "decision": "ALLOW"}
            ]
        }
    ]

    for a_data in agents_data:
        ag = db.query(Agent).filter(Agent.id == a_data["id"]).first()
        if not ag:
            ag = Agent(**a_data)
            db.add(ag)
        else:
            for k, v in a_data.items():
                setattr(ag, k, v)
    db.commit()

    # 4. Standard Governance Policies
    policies_data = [
        {
            "code": "POL_RESERVE_FLOOR",
            "name": "Mandatory Statutory Cash Reserve Floor",
            "description": "Requires merchant cash balance to remain strictly >= ₹5,00,000 at all times.",
            "policy_type": "RESERVE",
            "threshold_value": 500000.0,
            "operator": ">=",
            "severity": "CRITICAL",
            "is_active": True
        },
        {
            "code": "POL_MAX_SINGLE_TX",
            "name": "Single Autonomous Transaction Hard Ceiling",
            "description": "Caps any single autonomous AI agent action proposal at ₹5,00,000.",
            "policy_type": "SINGLE_TRANSACTION",
            "threshold_value": 500000.0,
            "operator": "<=",
            "severity": "HIGH",
            "is_active": True
        },
        {
            "code": "POL_DAILY_PAYOUT_CAP",
            "name": "Daily Cumulative Vendor Payout Ceiling",
            "description": "Limits daily cumulative supplier payouts to ₹8,00,000.",
            "policy_type": "DAILY_LIMIT",
            "threshold_value": 800000.0,
            "operator": "<=",
            "severity": "HIGH",
            "is_active": True
        },
        {
            "code": "POL_DAILY_REFUND_CAP",
            "name": "Daily Cumulative Customer Refund Ceiling",
            "description": "Limits daily cumulative customer refunds to ₹2,00,000.",
            "policy_type": "DAILY_LIMIT",
            "threshold_value": 200000.0,
            "operator": "<=",
            "severity": "HIGH",
            "is_active": True
        },
        {
            "code": "POL_DAILY_GROWTH_CAP",
            "name": "Daily Performance Marketing Budget Ceiling",
            "description": "Limits daily discretionary marketing ad-spend to ₹3,00,000.",
            "policy_type": "DAILY_LIMIT",
            "threshold_value": 300000.0,
            "operator": "<=",
            "severity": "MEDIUM",
            "is_active": True
        },
        {
            "code": "POL_AGENT_TRUST",
            "name": "Autonomous Agent Minimum Trust Threshold",
            "description": "Autonomous agents must maintain a trust score >= 60.0 to propose non-supervised actions.",
            "policy_type": "TRUST",
            "threshold_value": 60.0,
            "operator": ">=",
            "severity": "HIGH",
            "is_active": True
        }
    ]

    for p_data in policies_data:
        pol = db.query(Policy).filter(Policy.code == p_data["code"]).first()
        if not pol:
            pol = Policy(**p_data)
            db.add(pol)
        else:
            for k, v in p_data.items():
                setattr(pol, k, v)
    db.commit()

    # 5. Add historical ledger entries if none exist
    if db.query(TransactionLedger).count() == 0:
        sample_txs = [
            ("payout_agent", "PAYOUT", 150000.0, 600000.0, "Settlement to Primary Logistics Carrier #904", "SIM-TXN-INIT-01"),
            ("refund_agent", "REFUND", 4200.0, 750000.0, "Customer Return Order #8192 Reversal", "SIM-TXN-INIT-02"),
            ("growth_agent", "MARKETING_SPEND", 85000.0, 754200.0, "Google Performance Max Campaign Top-up", "SIM-TXN-INIT-03")
        ]
        for ag_id, t_type, amt, bal, desc, ref in sample_txs:
            t = TransactionLedger(
                merchant_id=merchant.id,
                agent_id=ag_id,
                transaction_type=t_type,
                amount=amt,
                balance_after=bal,
                description=desc,
                reference=ref,
                timestamp=datetime.utcnow() - timedelta(days=1)
            )
            db.add(t)
        db.commit()
