# FinGuard AI — Decision Flow & 10-Stage Pipeline

```
[ AI Agent Proposal ]
        │
        ▼
[ Stage 01: Action Gateway Interception & Identity Check ]
        │
        ▼
[ Stage 02: Financial Intent Extraction (ML Classification) ]
        │
        ▼
[ Stage 03: Policy Engine Evaluation (Reserve, Limits, Caps) ]
        │
        ▼
[ Stage 04: Financial State Engine (Cash, Reserve, Receivables) ]
        │
        ▼
[ Stage 05: Cross-Agent Conflict Engine (Global Concurrency) ]
        │
        ▼
[ Stage 06: Future Impact Prediction Engine (Liquidity Runway) ]
        │
        ▼
[ Stage 07: Multi-Factor Risk Assessment (0-100 ML Regressor) ]
        │
        ▼
[ Stage 08: Agent Dynamic Trust & Telemetry Profile ]
        │
        ▼
[ Stage 09: What-If Simulation Studio (Counterfactual Scenarios) ]
        │
        ▼
[ Stage 10: Safe Alternative Synthesis & Apex Adjudication ]
        │
        ├── ALLOW    ───► Direct Execution Simulator
        ├── DELAY    ───► Schedule Execution Window (+24h)
        ├── MODIFY   ───► Dual Human Authorization Queue
        ├── ESCALATE ───► Dual Human Authorization Queue
        └── BLOCK    ───► Immediate Rejection & Incident Log
        │
        ▼
[ Execution Record & Cryptographic Audit Receipt Minting ]
```

## Governance Decision Matrix

| Condition | Output Decision | Execution Action | Human Approval Required? |
| :--- | :--- | :--- | :--- |
| **All policies pass, Risk < 65, No cross-agent conflict, Free cash sufficient** | `ALLOW` | Immediate execution of full proposed amount | **No** (Autonomous) |
| **Global multi-agent conflict detected OR Reserve breached, but partial split feasible** | `MODIFY` | Split execution: Disburse safe amount now, defer balance | **Yes** (Dual Control) |
| **Low urgency, tight free cash, positive receivables arriving in 24h** | `DELAY` | Reschedule execution to next clearing window | **No** |
| **High risk score (>=65) OR High single value transaction within reserve** | `ESCALATE` | Escalate full amount to Treasury Reviewer | **Yes** (Dual Control) |
| **Critical policy violations (>=2) OR Agent Restricted OR Insolvency breach** | `BLOCK` | Cancel transaction outright; freeze agent privileges | **No** (Direct Block) |
