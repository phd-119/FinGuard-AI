# FIN GUARD AI

> **Financial Governance Control Plane for Autonomous AI Agents**  
> *Built for the Razorpay AI Builder Internship 2026 Buildathon.*

---

## 🌟 Executive Summary

**FinGuard AI** is an intelligent, unbypassable safety and governance control plane that sits between **Autonomous AI Agents** and **Financial Execution Systems**.

```
┌──────────────────────────┐      ┌──────────────────────────┐      ┌──────────────────────────┐
│   AUTONOMOUS AI AGENTS   │ ───► │      FIN GUARD AI        │ ───► │    FINANCIAL SYSTEM      │
│     Decision Makers      │      │ Governance & Safety Plane│      │     Execution Layer      │
└──────────────────────────┘      └──────────────────────────┘      └──────────────────────────┘
```

The fundamental principle:
1. **AI Agents** = Decision Makers (propose actions)
2. **FinGuard AI** = Governance + Safety + Global Reconciliation Layer (adjudicates actions)
3. **Financial System** = Execution Layer (simulated state movement)

> **Key Rule**: Autonomous AI agents must **NEVER** directly execute financial actions or hold raw payment API credentials. Every financial proposal must pass through the FinGuard Action Gateway.

---

## 💡 The Core Innovation: Global Multi-Agent Financial Governance

Most AI safety layers evaluate single agents in a silo. In enterprise finance, catastrophic risk arises when **multiple well-intentioned, uncoordinated autonomous agents submit actions simultaneously**.

### ⚠️ The Failure Scenario (Why Siloed Governance Fails):
- **Merchant Available Cash**: ₹6,00,000
- **Mandatory Minimum Reserve**: ₹5,00,000 (Required for payroll & regulatory solvency)
- **Unreserved Free Liquidity**: ₹1,00,000

| Proposing Agent | Proposed Action | Amount | Stated Agent Objective | Appears Safe in Silo? |
| :--- | :--- | :--- | :--- | :--- |
| **Payout Agent** | Supplier Settlement | **₹4,00,000** | Pay critical raw materials invoice | ✅ Yes (Cash is ₹6L) |
| **Growth Agent** | Performance Ad Spend | **₹2,00,000** | Q4 festive marketing campaign | ✅ Yes (Within budget) |
| **Refund Agent** | Customer Dispute Batch | **₹1,00,000** | Honor return SLA for defective batch | ✅ Yes (Normal refunds) |
| **TOTAL OUTFLOW** | **Simultaneous Outflow** | **₹7,00,000** | **Total capital demanded by fleet** | ❌ **INSOLVENCY BREACH** |

### 🛡️ How FinGuard Solves It:
Instead of evaluating proposals in isolation:
1. **Discovers Concurrent Load**: Detects that aggregate proposed outflow (₹7,00,000) exceeds total cash (₹6,00,000) and triggers a **₹6,00,000 statutory reserve shortfall**.
2. **Calculates Multi-Factor Risk**: Evaluates risk score at **87/100 (Critical Risk)** via trained ML regression.
3. **Simulates Counterfactual What-Ifs**: Compares immediate execution, split execution, delay, and block.
4. **Synthesizes Constructive Alternative**: Rather than a dumb block, it generates a **`MODIFY`** decision:
   - Disburse **₹1,00,000 immediately** (utilizing all available free liquidity to satisfy the urgent supplier milestone).
   - Defer **₹3,00,000 by 24 hours** until scheduled receivables arrive.
5. **Enforces Dual Human Signoff**: Routes to Treasury Reviewer for verification.
6. **Safe Execution & Cryptographic Audit**: State is updated to **₹5,00,000 (Reserve 100% Intact)**, and a SHA-256 verified receipt is minted.

---

## 🏗️ The 10-Stage FinGuard Governance Pipeline

Every proposal follows this complete, unbypassable flow:

```
[ AI Agent Proposal ]
        │
        ▼
[ 1. Action Gateway ] ──────────► Validates agent identity, permissions, and schema bounds
        │
        ▼
[ 2. Financial Intent Engine ] ─► ML classification of commercial purpose and cashflow vector
        │
        ▼
[ 3. Policy Engine ] ───────────► Evaluates statutory reserve floor, transaction caps, velocity
        │
        ▼
[ 4. Financial State Engine ] ──► Queries real-time cash, reserve buffers, payables, receivables
        │
        ▼
[ 5. Conflict Engine ] ─────────► CORE INNOVATION: Detects multi-agent global liquidity collisions
        │
        ▼
[ 6. Prediction Engine ] ───────► Forecasts projected cash runway and reserve degradation
        │
        ▼
[ 7. Risk Engine ] ─────────────► Multi-factor Gradient Boosting regression (0-100 risk score)
        │
        ▼
[ 8. Agent Trust Engine ] ──────► Tracks historical compliance, violation rate, dynamic trust score
        │
        ▼
[ 9. Simulation Studio ] ───────► Evaluates 4 counterfactual scenarios across liquidity curves
        │
        ▼
[ 10. Safe Alternative & Decision ] ──► Derives: ALLOW | MODIFY | DELAY | ESCALATE | BLOCK
        │
        ▼
[ Dual Human Approval (if required) ] ──► Human review and signoff for modified/escalated actions
        │
        ▼
[ Financial Execution Simulator ] ────► Updates merchant ledger and balance (sandbox environment)
        │
        ▼
[ Immutable Audit Trail ] ────────────► Cryptographic decision receipt with explainability rationale
```

---

## 🤖 The Autonomous AI Agents Fleet

FinGuard ships with 5 simulated specialized financial AI agents:

1. **Payout Agent** (`payout_agent`): Optimizes supplier/vendor payouts while preserving liquidity and credit terms.
2. **Refund Agent** (`refund_agent`): Processes customer returns, chargebacks, and goodwill refunds adhering to policy limits.
3. **Growth Agent** (`growth_agent`): Dynamically allocates paid advertising budgets across high-ROI acquisition channels.
4. **Collections Agent** (`collections_agent`): Accelerates cash collections and offers early settlement incentives for receivables.
5. **Treasury Agent** (`treasury_agent`): Manages overnight float sweeps, liquidity buffers, and statutory reserve compliance.

---

## 🧠 AI / ML Architecture & Methodology

FinGuard avoids "fake AI" outputs. It employs real, trained scikit-learn models serialized in `ml/models/` with statistical failover bounds:

- **Financial Intent Classifier** (`intent_classifier.joblib`): TF-IDF n-gram vectorizer + Logistic Regression trained on commercial transactions (100% test accuracy).
- **Multi-Factor Risk Scorer Regressor** (`risk_scorer.joblib`): Gradient Boosting Regressor predicting continuous risk (0-100) based on liquidity ratios, concurrency severity, policy violations, and agent trust (R² = 0.991, RMSE = 2.518).
- **Governance Decision Classifier** (`decision_classifier.joblib`): Random Forest classifier modeling optimal governance actions (99.5% accuracy).

---

## 🚀 Quickstart & Installation

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11.9)
- **Node.js 18+** & **npm** (Tested on Node v24 / npm 11)

### 1. Clone & Setup Backend
```bash
git clone https://github.com/your-username/finguard-ai.git
cd finguard-ai

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain ML models from scratch
python ml/data/generate_synthetic_data.py
python ml/training/train_models.py
```

### 2. Run Backend Server
```bash
# From repository root
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Backend API docs will be live at `http://localhost:8000/docs`.*

### 3. Setup & Run Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend control plane dashboard will be live at `http://localhost:5173`.*

---

## 🧪 Running the Test Suite

Execute the comprehensive automated test suite (27 unit, engine, live API, and end-to-end integration tests):

```bash
# Run pytest from repository root
python -m pytest backend/tests -v
```

### Verified Test Results:
```
backend/tests/test_all_endpoints_live.py::test_system_health PASSED      [  3%]
backend/tests/test_all_endpoints_live.py::test_merchants_api PASSED      [  7%]
backend/tests/test_all_endpoints_live.py::test_agents_api PASSED         [ 11%]
backend/tests/test_all_endpoints_live.py::test_financial_state_api PASSED [ 14%]
backend/tests/test_all_endpoints_live.py::test_policies_api PASSED       [ 18%]
backend/tests/test_all_endpoints_live.py::test_action_gateway_propose_and_reasoning PASSED [ 22%]
backend/tests/test_all_endpoints_live.py::test_conflicts_and_risk_api PASSED [ 25%]
backend/tests/test_all_endpoints_live.py::test_approvals_and_audit_api PASSED [ 29%]
backend/tests/test_all_endpoints_live.py::test_hero_demo_flow PASSED     [ 33%]
backend/tests/test_api.py::test_health_and_root PASSED                   [ 37%]
backend/tests/test_api.py::test_merchants_endpoints PASSED               [ 40%]
backend/tests/test_api.py::test_agents_endpoints PASSED                  [ 44%]
backend/tests/test_api.py::test_financial_state_and_health_endpoints PASSED [ 48%]
backend/tests/test_api.py::test_policies_endpoints PASSED                [ 51%]
backend/tests/test_api.py::test_action_gateway_rejects_unauthorized_agent PASSED [ 55%]
backend/tests/test_engines.py::test_action_gateway_validation PASSED     [ 59%]
backend/tests/test_engines.py::test_intent_engine PASSED                 [ 62%]
backend/tests/test_engines.py::test_policy_engine_reserve_compliance PASSED [ 66%]
backend/tests/test_engines.py::test_conflict_engine_detection PASSED     [ 70%]
backend/tests/test_engines.py::test_optimization_engine_split_and_multi_agent PASSED [ 74%]
backend/tests/test_engines.py::test_simulation_and_alternative_engine PASSED [ 77%]
backend/tests/test_hero_demo.py::test_hero_demo_flow_end_to_end PASSED   [ 81%]
backend/tests/test_pipeline.py::test_governance_pipeline_allow_flow PASSED [ 85%]
backend/tests/test_pipeline.py::test_governance_pipeline_modify_flow PASSED [ 88%]
backend/tests/test_pipeline.py::test_governance_pipeline_delay_flow PASSED [ 92%]
backend/tests/test_pipeline.py::test_governance_pipeline_escalate_flow PASSED [ 96%]
backend/tests/test_pipeline.py::test_governance_pipeline_block_flow PASSED [100%]
======================== 27 passed, 1 warning in 1.99s ========================
```

---

## 🎬 How to Run the Hero Demo

1. Open `http://localhost:5173` in your browser.
2. Click the green **"Run FinGuard Demo"** button on the Dashboard, or click the **"Hero Demo"** navigation tab.
3. Click through the 4 interactive stages:
   - **Stage 1**: Observe initial state (₹6L Cash, ₹5L Reserve, ₹1L Free Liquidity).
   - **Stage 2**: Inspect discovered background agents (Growth ₹2L, Refund ₹1L) colliding with Payout Agent (₹4L).
   - **Stage 3**: Inspect FinGuard's 10-stage reasoning chain and derived **`MODIFY`** decision (₹1L immediate + ₹3L deferred).
   - **Stage 4**: Click **"Sign & Execute Governed Action"** to approve the modified transaction. Verify that the merchant cash settles at **₹5,00,000 (Reserve 100% Intact)** and a cryptographic audit receipt is minted.

*Detailed Integration Verification Report is available in [docs/INTEGRATION_VERIFICATION.md](docs/INTEGRATION_VERIFICATION.md).*

---

## 📄 License
Released under the [MIT License](LICENSE).
