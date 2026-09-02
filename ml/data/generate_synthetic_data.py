"""
FinGuard AI - Synthetic ML Data Generator
Generates realistic training datasets for:
1. Financial Intent Classification
2. Risk Scoring & Breach Prediction
3. Cash Flow Forecasting / Liquidity Stress
"""

import json
import os
import random
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_intent_dataset(n_samples=2500):
    """
    Generate dataset for intent classification from action proposals.
    Classes:
    - SUPPLIER_SETTLEMENT (Payout Agent)
    - CUSTOMER_REFUND (Refund Agent)
    - GROWTH_INVESTMENT (Growth Agent)
    - DEBT_COLLECTION (Collections Agent)
    - LIQUIDITY_REBALANCE (Treasury Agent)
    """
    templates = {
        "SUPPLIER_SETTLEMENT": [
            "Payment for Q3 vendor invoices regarding cloud infrastructure",
            "Settlement of raw material invoice #{id} to primary vendor",
            "Disbursement for logistics partner freight clearing",
            "Routine bi-weekly supplier invoice settlement for inventory batch #{id}",
            "Vendor payout for contract software engineering services",
            "Urgent payment to critical supplier to release pending shipment",
            "Quarterly supplier retention bonus and milestone settlement",
            "Payment of hardware maintenance contract for warehouse {id}"
        ],
        "CUSTOMER_REFUND": [
            "Customer refund for damaged shipment order #{id}",
            "Subscription cancellation charge reversal requested by user",
            "Double charge correction and dispute refund for transaction #{id}",
            "Goodwill refund for delayed order delivery breach SLA",
            "Full refund for returned defective electronic unit #{id}",
            "Partial refund due to discount coupon error at checkout",
            "Chargeback resolution and customer refund reconciliation",
            "Merchant store credit conversion to original payment refund"
        ],
        "GROWTH_INVESTMENT": [
            "Performance marketing ad spend allocation on Google Ads",
            "Influencer campaign budget deposit for festive season launch",
            "Paid acquisition ad spend top-up on Meta and LinkedIn",
            "Search engine marketing budget expansion for high-intent keywords",
            "Sponsorship fee for national fintech developer conference",
            "Brand awareness campaign media buying for Q4",
            "Affiliate partner commission prepayment for festival sprint",
            "Customer referral bonus pool allocation"
        ],
        "DEBT_COLLECTION": [
            "Early settlement discount incentive to collect overdue receivable",
            "Collection agency recovery contingency disbursement",
            "Automated payment gateway collection retry incentive",
            "Legal notice issuance fee for delinquent enterprise account #{id}",
            "Receivable discount fee for accelerated factoring liquidation",
            "Follow-up collection workflow trigger with dynamic discount #{id}",
            "Settlement waiver allocation for 90-day overdue merchant balance",
            "Escrow account setup for disputed receivable recovery"
        ],
        "LIQUIDITY_REBALANCE": [
            "Yield optimization sweep of idle float to overnight liquid funds",
            "Replenishment of working capital escrow reserve buffer",
            "Inter-account treasury transfer from primary current to payroll reserve",
            "Short-term liquid mutual fund redemption to bolster working cash",
            "Hedging collateral deposit for forex currency fluctuations",
            "Treasury rebalancing to maintain regulatory statutory reserve buffer",
            "Liquidity pool re-allocation across multi-banking nodal accounts",
            "Emergency reserve replenishment following high outflow cycle"
        ]
    }

    records = []
    for _ in range(n_samples):
        intent = random.choice(list(templates.keys()))
        tmpl = random.choice(templates[intent])
        desc = tmpl.format(id=random.randint(1000, 9999))
        
        agent_map = {
            "SUPPLIER_SETTLEMENT": "Payout Agent",
            "CUSTOMER_REFUND": "Refund Agent",
            "GROWTH_INVESTMENT": "Growth Agent",
            "DEBT_COLLECTION": "Collections Agent",
            "LIQUIDITY_REBALANCE": "Treasury Agent"
        }
        
        amount_ranges = {
            "SUPPLIER_SETTLEMENT": (50000, 800000),
            "CUSTOMER_REFUND": (1000, 150000),
            "GROWTH_INVESTMENT": (50000, 500000),
            "DEBT_COLLECTION": (5000, 100000),
            "LIQUIDITY_REBALANCE": (100000, 1500000)
        }
        
        low, high = amount_ranges[intent]
        amount = round(random.uniform(low, high), 2)
        urgency = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        
        records.append({
            "description": desc,
            "agent_name": agent_map[intent],
            "amount": amount,
            "urgency": urgency,
            "intent_label": intent
        })
        
    df = pd.DataFrame(records)
    path = os.path.join(DATA_DIR, "intent_dataset.csv")
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} intent samples to {path}")
    return df


def generate_risk_dataset(n_samples=4000):
    """
    Generate dataset for multi-factor risk assessment and breach prediction.
    """
    records = []
    for _ in range(n_samples):
        available_cash = random.uniform(200000, 2000000)
        required_reserve = random.uniform(150000, 1500000)
        if required_reserve > available_cash * 0.9:
            required_reserve = available_cash * 0.8
            
        amount = random.uniform(10000, 1200000)
        pending_concurrent_outflows = random.uniform(0, 800000)
        agent_trust_score = random.uniform(40, 99)
        agent_confidence = random.uniform(0.60, 0.99)
        policy_violations = random.choices([0, 1, 2, 3], weights=[0.7, 0.18, 0.08, 0.04])[0]
        urgency_val = random.choice([1.0, 2.0, 3.0, 4.0])
        
        liquidity_ratio_before = available_cash / max(required_reserve, 1.0)
        total_proposed_outflow = amount + pending_concurrent_outflows
        post_execution_cash = available_cash - amount
        post_global_cash = available_cash - total_proposed_outflow
        
        projected_liquidity_ratio = max(0.0, post_execution_cash / max(required_reserve, 1.0))
        global_projected_liquidity_ratio = max(0.0, post_global_cash / max(required_reserve, 1.0))
        reserve_shortfall = max(0.0, required_reserve - post_global_cash)
        
        if post_global_cash < required_reserve and pending_concurrent_outflows > 50000:
            cross_agent_conflict_severity = min(1.0, (required_reserve - post_global_cash) / required_reserve + 0.3)
        elif total_proposed_outflow > available_cash * 0.6:
            cross_agent_conflict_severity = random.uniform(0.2, 0.5)
        else:
            cross_agent_conflict_severity = random.uniform(0.0, 0.15)
            
        threat_ratio = (amount + pending_concurrent_outflows) / max(1.0, (available_cash - required_reserve + 1e-5))
        f_reserve = min(35.0, max(0.0, (1.0 - global_projected_liquidity_ratio) * 35.0)) if global_projected_liquidity_ratio < 1.0 else min(15.0, threat_ratio * 10.0)
        
        free_cash = max(1000.0, available_cash - required_reserve)
        f_amount = min(25.0, (amount / free_cash) * 20.0)
        f_conflict = cross_agent_conflict_severity * 20.0
        f_policy = policy_violations * 5.0
        f_trust = (80.0 - agent_trust_score) * 0.25
        
        raw_risk = f_reserve + f_amount + f_conflict + f_policy + f_trust + random.normalvariate(0, 2.0)
        risk_score = round(float(np.clip(raw_risk, 2.0, 98.0)), 1)
        
        if risk_score >= 80.0:
            category = "CRITICAL"
        elif risk_score >= 60.0:
            category = "HIGH"
        elif risk_score >= 35.0:
            category = "MEDIUM"
        else:
            category = "LOW"
            
        if policy_violations >= 2 or post_execution_cash < 0:
            decision = "BLOCK"
        elif cross_agent_conflict_severity > 0.6 or (post_global_cash < required_reserve and amount > 100000):
            decision = "MODIFY"
        elif risk_score >= 75.0 or (urgency_val >= 3.0 and risk_score >= 60.0):
            decision = "ESCALATE"
        elif urgency_val <= 2.0 and risk_score >= 50.0:
            decision = "DELAY"
        else:
            decision = "ALLOW"
            
        records.append({
            "amount": amount,
            "available_cash": available_cash,
            "required_reserve": required_reserve,
            "pending_concurrent_outflows": pending_concurrent_outflows,
            "agent_trust_score": agent_trust_score,
            "agent_confidence": agent_confidence,
            "policy_violations": policy_violations,
            "urgency_score": urgency_val,
            "liquidity_ratio_before": round(liquidity_ratio_before, 3),
            "projected_liquidity_ratio": round(projected_liquidity_ratio, 3),
            "global_projected_liquidity_ratio": round(global_projected_liquidity_ratio, 3),
            "reserve_shortfall": round(reserve_shortfall, 2),
            "cross_agent_conflict_severity": round(cross_agent_conflict_severity, 3),
            "risk_score": risk_score,
            "risk_category": category,
            "recommended_decision": decision
        })
        
    df = pd.DataFrame(records)
    path = os.path.join(DATA_DIR, "risk_dataset.csv")
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} risk samples to {path}")
    return df

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    generate_intent_dataset()
    generate_risk_dataset()
