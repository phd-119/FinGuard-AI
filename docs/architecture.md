# FinGuard AI — System Architecture

## 1. Architectural Overview

**FinGuard AI** is a specialized financial safety and governance control plane designed to sit strictly between **Autonomous AI Agents** (decision makers) and **Financial Execution Systems** (payment gateways, bank rails, nodal escrow accounts).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       AUTONOMOUS AI AGENTS                              │
│  [ Payout Agent ]  [ Refund Agent ]  [ Growth Agent ]  [ Treasury Agent ]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Proposes Action)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 FINGUARD ACTION GATEWAY (UNBYPASSABLE)                  │
│   • Identity Verification  • Agent Permission Matrix  • Schema Bounds   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 FINGUARD 10-STAGE GOVERNANCE PIPELINE                   │
│                                                                         │
│  Stage 01: Agent Action Proposal Interception                           │
│  Stage 02: Financial Intent Engine (ML Classification)                  │
│  Stage 03: Policy Compliance Engine (Reserve, Transaction, Velocity)    │
│  Stage 04: Current Merchant Financial State Engine                      │
│  Stage 05: Cross-Agent Conflict Engine (Global Multi-Agent Matrix)      │
│  Stage 06: Future Impact & Liquidity Forecast Engine                    │
│  Stage 07: Multi-Factor Risk Assessment Engine (ML Regressor 0-100)     │
│  Stage 08: Agent Dynamic Trust & Telemetry Profile                      │
│  Stage 09: What-If Simulation Studio (Counterfactual Scenarios)         │
│  Stage 10: Safe Alternative Synthesis & Governance Decision             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
        [ ALLOW / DELAY ]                       [ MODIFY / ESCALATE ]
                 │                                       │
                 ▼                                       ▼
        [ Direct Safe Exec ]                    [ Dual Human Signoff ]
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 FINANCIAL EXECUTION SIMULATOR & LEDGER                  │
│       • Safe State Balance Update  • Cryptographic Receipt Minting      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 IMMUTABLE AUDIT TRAIL & DECISION RECEIPT                │
│    Receipt #FG-RCPT-XXXXXX • SHA-256 Hash • Explainability Record       │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. Core Engine Components

### 2.1 Action Gateway
- **Entrypoint**: Intercepts all proposals via `POST /api/v1/actions/propose`.
- **Security Rule**: AI agents possess no payment API credentials or execution pathways. Direct money movement is physically impossible.

### 2.2 Financial Intent Engine
- **Model**: TF-IDF Vectorizer + Multinomial / Logistic Classifier (`intent_classifier.joblib`) trained on commercial transaction telemetry.
- **Output**: Intent Category (e.g. `SUPPLIER_SETTLEMENT`, `CUSTOMER_REFUND`, `GROWTH_INVESTMENT`), business urgency, operational purpose vector.

### 2.3 Policy Engine
- **Enforcement**: Evaluates statutory reserve floor, single transaction limits, daily caps, and agent permission rules.

### 2.4 Cross-Agent Conflict Engine (Core Innovation)
- **Problem**: Individual autonomous agents optimize isolated objectives without visibility into peer agent plans.
- **Solution**: FinGuard inspects the global concurrent queue of all pending actions, calculates total aggregate proposed outflow, and models collective impact against merchant cash reserves.

### 2.5 Risk & Trust Engines
- **Risk Regressor**: Gradient Boosting Regressor (`risk_scorer.joblib`) evaluating amount, unreserved free liquidity, multi-agent concurrency severity, and policy violations.
- **Trust Tracker**: Dynamic reputation scoring (0-100) reflecting agent compliance history and anomaly frequency.

### 2.6 What-If Simulation & Alternative Generation
- Simulates 4 counterfactual paths:
  1. Full immediate execution
  2. Governed split execution (safe immediate + deferred balance)
  3. Reschedule (+24h)
  4. Block & cancel
- Recommends the safest feasible option that maintains the statutory reserve floor.

### 2.7 Decision Engine & Human Dual Control
- Adjudicates the proposal into: `ALLOW`, `MODIFY`, `DELAY`, `ESCALATE`, or `BLOCK`.
- If modified or high-risk, routes to the Human Approval Queue for dual authorization.
