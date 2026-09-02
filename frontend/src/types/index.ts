export interface HealthStatus {
  status: string;
  version: string;
  control_plane: string;
  timestamp: string;
}

export interface Agent {
  id: string;
  name: string;
  agent_type: string;
  objective: string;
  trust_score: number;
  trust_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'VERIFIED' | 'RESTRICTED';
  status: 'ACTIVE' | 'PAUSED' | 'RESTRICTED';
  total_proposals: number;
  approved_proposals: number;
  modified_proposals: number;
  blocked_proposals: number;
  violation_count: number;
  historical_telemetry: Array<{
    timestamp: string;
    action: string;
    amount: number;
    decision: string;
  }>;
}

export interface FinancialState {
  id: string;
  merchant_id: string;
  cash_balance: number;
  available_balance: number;
  reserved_balance: number;
  reserve_requirement: number;
  daily_inflows: number;
  daily_outflows: number;
  pending_payouts: number;
  pending_refunds: number;
  receivables: number;
  payables: number;
  marketing_spend: number;
  liquidity_ratio: number;
  updated_at: string;
}

export interface Policy {
  id: string;
  code: string;
  name: string;
  description: string;
  policy_type: string;
  threshold_value: number;
  operator: string;
  severity: 'WARNING' | 'HIGH' | 'CRITICAL';
  is_active: boolean;
}

export interface PolicyCheckResult {
  policy_code: string;
  policy_name: string;
  is_compliant: boolean;
  threshold: number;
  actual_value: number;
  severity: string;
  message: string;
}

export interface IntentClassificationResult {
  intent_label: string;
  purpose: string;
  urgency: string;
  financial_effect: string;
  confidence: number;
  explanation: string;
}

export interface DetectedAgentSummary {
  agent_id: string;
  agent_name: string;
  action_type: string;
  amount: number;
  urgency: string;
  priority: number;
  reason: string;
  is_current_subject: boolean;
}

export interface ConflictDetectionResult {
  conflict_detected: boolean;
  conflict_type: string;
  severity: 'NONE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  detected_agents: DetectedAgentSummary[];
  aggregate_outflow: number;
  available_cash: number;
  required_reserve: number;
  projected_shortfall: number;
  explanation: string;
}

export interface FutureImpactResult {
  projected_cash: number;
  projected_reserve: number;
  reserve_shortfall: number;
  projected_liquidity_ratio: number;
  future_cash_pressure: string;
  expected_runway_days: number;
  confidence: number;
  explanation: string;
}

export interface RiskAssessmentResult {
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_factors: string[];
  model_confidence: number;
  explanation: string;
}

export interface AgentTrustResult {
  agent_id: string;
  trust_score: number;
  trust_level: string;
  historical_proposals: number;
  violation_rate: number;
  factors: string[];
}

export interface ScenarioComparison {
  scenario_id: string;
  name: string;
  description: string;
  immediate_outflow: number;
  deferred_outflow: number;
  remaining_cash: number;
  reserve_shortfall: number;
  liquidity_ratio: number;
  risk_score: number;
  policy_compliant: boolean;
  is_recommended: boolean;
}

export interface SafeAlternativeResult {
  alternative_type: string;
  immediate_amount: number;
  deferred_amount: number;
  delay_hours: number;
  recommended_action: string;
  rationale: string;
}

export interface GovernanceDecisionResult {
  decision: 'ALLOW' | 'MODIFY' | 'DELAY' | 'ESCALATE' | 'BLOCK';
  decision_reason: string;
  recommended_action: string;
  modified_amount: number | null;
  deferred_amount: number | null;
  delay_hours: number;
  risk_level: string;
  confidence: number;
  supporting_factors: string[];
  requires_human_approval: boolean;
}

export interface EvaluationPipelineResponse {
  proposal_id: string;
  agent_id: string;
  agent_name: string;
  original_amount: number;
  action_type: string;
  status: string;
  timestamp: string;
  intent: IntentClassificationResult;
  policy_checks: PolicyCheckResult[];
  conflict: ConflictDetectionResult;
  future_impact: FutureImpactResult;
  risk_assessment: RiskAssessmentResult;
  trust_profile: AgentTrustResult;
  what_if_scenarios: ScenarioComparison[];
  safe_alternative: SafeAlternativeResult;
  decision: GovernanceDecisionResult;
}

export interface ProposalSummary {
  id: string;
  agent_id: string;
  agent_name: string;
  action_type: string;
  amount: number;
  currency: string;
  urgency: string;
  priority: number;
  status: string;
  final_decision: string | null;
  risk_score: number | null;
  risk_level: string | null;
  conflict_severity: string | null;
  reason: string;
  created_at: string;
}

export interface PendingApproval {
  approval_id: string;
  proposal_id: string;
  agent_id: string;
  agent_name: string;
  action_type: string;
  original_amount: number;
  recommended_amount: number;
  deferred_amount: number;
  governance_decision: string;
  decision_reason: string;
  risk_score: number;
  risk_level: string;
  conflict_detected: boolean;
  requested_at: string;
  comments: string | null;
}

export interface AuditReceipt {
  receipt_number: string;
  action_hash: string;
  proposal_id: string;
  agent_id: string;
  agent_name: string;
  original_amount: number;
  approved_amount: number;
  governance_decision: string;
  risk_score: number;
  conflict_detected: boolean;
  conflict_summary: string | null;
  human_approver: string | null;
  execution_status: string;
  decision_rationale: string;
  timestamp: string;
  full_reasoning_payload: Record<string, any>;
}

export interface LedgerTransaction {
  id: string;
  merchant_id: string;
  agent_id: string;
  proposal_id: string | null;
  transaction_type: string;
  amount: number;
  balance_after: number;
  description: string;
  reference: string;
  timestamp: string;
}
