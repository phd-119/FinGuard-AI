"""
FinGuard AI - Pydantic Request & Response Schemas
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# --- Base & Generic ---
class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    control_plane: str = "FIN_GUARD_PROTECTED"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# --- Merchant Schemas ---
class MerchantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    id: str
    name: str
    business_category: str
    created_at: datetime
    cash_balance: Optional[float] = None
    reserve_requirement: Optional[float] = None
    available_balance: Optional[float] = None

class MerchantCreate(BaseModel):
    name: str = "OmniRetail D2C India"
    business_category: str = "E-Commerce / D2C"
    initial_cash: float = 600000.0
    reserve_requirement: float = 500000.0

# --- Agent Schemas ---
class AgentBase(BaseModel):
    id: str
    name: str
    agent_type: str
    objective: str
    trust_score: float = 85.0
    trust_level: str = "HIGH"
    status: str = "ACTIVE"

class AgentDetail(AgentBase):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    total_proposals: int = 0
    approved_proposals: int = 0
    modified_proposals: int = 0
    blocked_proposals: int = 0
    violation_count: int = 0
    historical_telemetry: List[Dict[str, Any]] = []

# --- Financial State Schemas ---
class FinancialStateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    id: str
    merchant_id: str
    cash_balance: float
    available_balance: float
    reserved_balance: float
    reserve_requirement: float
    daily_inflows: float
    daily_outflows: float
    pending_payouts: float
    pending_refunds: float
    receivables: float
    payables: float
    marketing_spend: float
    liquidity_ratio: float
    updated_at: datetime

class FinancialStateUpdate(BaseModel):
    cash_balance: Optional[float] = None
    reserve_requirement: Optional[float] = None
    daily_inflows: Optional[float] = None
    daily_outflows: Optional[float] = None

class PendingOutflowRequest(BaseModel):
    agent_id: str
    amount: float
    action_type: str = "PAYOUT"
    reason: Optional[str] = "Pending outflow allocation"

class FinancialHealthOut(BaseModel):
    merchant_id: str
    status: str = "HEALTHY"
    cash_balance: float
    reserve_requirement: float
    free_liquidity: float
    liquidity_ratio: float
    runway_days: int
    system_status: str = "FIN_GUARD_PROTECTED"

# --- Policy Schemas ---
class PolicyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    id: str
    code: str
    name: str
    description: str
    policy_type: str
    threshold_value: float
    operator: str
    severity: str
    is_active: bool

class PolicyCheckResult(BaseModel):
    policy_code: str
    policy_name: str
    is_compliant: bool
    threshold: float
    actual_value: float
    severity: str
    message: str

# --- Proposal & Gateway Schemas ---
class ProposeActionRequest(BaseModel):
    agent_id: str = Field(..., description="Unique agent identifier (e.g. payout_agent)")
    merchant_id: Optional[str] = Field(None, description="Merchant ID or defaults to active demo merchant")
    action_type: str = Field(..., description="Action type: PAYOUT, REFUND, MARKETING_SPEND, DEBT_RECOVERY, TREASURY_SWEEP")
    amount: float = Field(..., gt=0, description="Proposed amount in INR")
    currency: str = Field("INR", description="Currency symbol")
    urgency: str = Field("MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    priority: int = Field(3, ge=1, le=5, description="Priority level 1-5")
    confidence: float = Field(0.90, ge=0.0, le=1.0, description="Agent confidence score")
    reason: str = Field(..., min_length=5, description="Business rationale explaining the proposed action")
    raw_payload: Optional[Dict[str, Any]] = Field(default_factory=dict)

# --- Engine Outputs ---
class IntentClassificationResult(BaseModel):
    intent_label: str
    purpose: str
    urgency: str
    financial_effect: str
    confidence: float
    explanation: str

class ConflictDetectionResult(BaseModel):
    conflict_detected: bool
    conflict_type: str
    severity: str
    detected_agents: List[Dict[str, Any]]
    aggregate_outflow: float
    available_cash: float
    required_reserve: float
    projected_shortfall: float
    explanation: str

class FutureImpactResult(BaseModel):
    projected_cash: float
    projected_reserve: float
    reserve_shortfall: float
    projected_liquidity_ratio: float
    future_cash_pressure: str
    expected_runway_days: int
    confidence: float
    explanation: str

class RiskAssessmentResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    risk_score: float
    risk_level: str
    risk_factors: List[str]
    model_confidence: float
    explanation: str

class AgentTrustResult(BaseModel):
    agent_id: str
    trust_score: float
    trust_level: str
    historical_proposals: int
    violation_rate: float
    factors: List[str]

class ScenarioComparison(BaseModel):
    scenario_id: str
    name: str
    description: str
    immediate_outflow: float
    deferred_outflow: float
    remaining_cash: float
    reserve_shortfall: float
    liquidity_ratio: float
    risk_score: float
    policy_compliant: bool
    is_recommended: bool

class SafeAlternativeResult(BaseModel):
    alternative_type: str
    immediate_amount: float
    deferred_amount: float
    delay_hours: int
    recommended_action: str
    rationale: str

class GovernanceDecisionResult(BaseModel):
    decision: str
    decision_reason: str
    recommended_action: str
    modified_amount: Optional[float] = None
    deferred_amount: Optional[float] = None
    delay_hours: int = 0
    risk_level: str
    confidence: float
    supporting_factors: List[str]
    requires_human_approval: bool

# --- Full Evaluation Summary ---
class EvaluationPipelineResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    proposal_id: str
    agent_id: str
    agent_name: str
    original_amount: float
    action_type: str
    status: str
    timestamp: datetime
    
    intent: IntentClassificationResult
    policy_checks: List[PolicyCheckResult]
    conflict: ConflictDetectionResult
    future_impact: FutureImpactResult
    risk_assessment: RiskAssessmentResult
    trust_profile: AgentTrustResult
    what_if_scenarios: List[ScenarioComparison]
    safe_alternative: SafeAlternativeResult
    decision: GovernanceDecisionResult

# --- Human Approval & Execution ---
class HumanApprovalRequest(BaseModel):
    human_reviewer: str = "Treasury Lead"
    decision: str = Field(..., description="APPROVE, REJECT, or MODIFY_APPROVE")
    approved_amount: Optional[float] = None
    comments: Optional[str] = None

class ExecutionResultOut(BaseModel):
    execution_id: str
    proposal_id: str
    status: str
    executed_amount: float
    transaction_reference: str
    pre_execution_cash: float
    post_execution_cash: float
    pre_execution_reserve: float
    post_execution_reserve: float
    executed_at: datetime
    message: str

# --- Audit Receipt ---
class AuditReceiptOut(BaseModel):
    receipt_number: str
    action_hash: str
    proposal_id: str
    agent_id: str
    agent_name: str
    original_amount: float
    approved_amount: float
    governance_decision: str
    risk_score: float
    conflict_detected: bool
    conflict_summary: Optional[str]
    human_approver: Optional[str]
    execution_status: str
    decision_rationale: str
    timestamp: datetime
    full_reasoning_payload: Dict[str, Any]

# --- Proposal Summary for Table Views ---
class ProposalSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    id: str
    agent_id: str
    agent_name: str
    action_type: str
    amount: float
    currency: str
    urgency: str
    priority: int
    status: str
    final_decision: Optional[str]
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    conflict_severity: Optional[str] = None
    reason: str
    created_at: datetime

# --- Hero Demo Schemas ---
class HeroDemoStatus(BaseModel):
    step: int
    step_name: str
    description: str
    current_state: Dict[str, Any]
    evaluation: Optional[EvaluationPipelineResponse] = None
    audit_receipt: Optional[AuditReceiptOut] = None
