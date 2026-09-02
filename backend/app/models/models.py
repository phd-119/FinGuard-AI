"""
FinGuard AI - SQLAlchemy Data Models
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Boolean, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, default="OmniRetail D2C India")
    business_category = Column(String(50), default="E-Commerce / D2C")
    created_at = Column(DateTime, default=datetime.utcnow)

    financial_state = relationship("FinancialState", back_populates="merchant", uselist=False)
    proposals = relationship("AgentProposal", back_populates="merchant")


class FinancialState(Base):
    __tablename__ = "financial_states"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    merchant_id = Column(String(36), ForeignKey("merchants.id"), unique=True)
    
    cash_balance = Column(Float, default=600000.0)         # Total ledger cash
    available_balance = Column(Float, default=100000.0)    # Cash above required reserve
    reserved_balance = Column(Float, default=500000.0)     # Currently locked/held reserve
    reserve_requirement = Column(Float, default=500000.0)  # Mandatory regulatory/business reserve
    
    daily_inflows = Column(Float, default=120000.0)
    daily_outflows = Column(Float, default=45000.0)
    pending_payouts = Column(Float, default=0.0)
    pending_refunds = Column(Float, default=0.0)
    receivables = Column(Float, default=350000.0)
    payables = Column(Float, default=480000.0)
    marketing_spend = Column(Float, default=85000.0)
    liquidity_ratio = Column(Float, default=1.20)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    merchant = relationship("Merchant", back_populates="financial_state")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(String(50), primary_key=True) # e.g. "payout_agent"
    name = Column(String(100), nullable=False)
    agent_type = Column(String(50), nullable=False)
    objective = Column(Text, nullable=False)
    trust_score = Column(Float, default=85.0)  # 0 to 100
    trust_level = Column(String(20), default="HIGH") # LOW, MEDIUM, HIGH, VERIFIED
    status = Column(String(20), default="ACTIVE") # ACTIVE, PAUSED, RESTRICTED
    
    total_proposals = Column(Integer, default=0)
    approved_proposals = Column(Integer, default=0)
    modified_proposals = Column(Integer, default=0)
    blocked_proposals = Column(Integer, default=0)
    violation_count = Column(Integer, default=0)
    
    historical_telemetry = Column(JSON, default=list) # List of past action summaries
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    proposals = relationship("AgentProposal", back_populates="agent")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    policy_type = Column(String(50), nullable=False) # RESERVE, SINGLE_TRANSACTION, DAILY_LIMIT, CONFLICT, TRUST
    threshold_value = Column(Float, nullable=False)
    operator = Column(String(10), default="<=") # <=, >=, ==, <, >
    severity = Column(String(20), default="CRITICAL") # WARNING, HIGH, CRITICAL
    is_active = Column(Boolean, default=True)


class AgentProposal(Base):
    __tablename__ = "agent_proposals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_id = Column(String(50), ForeignKey("agents.id"), nullable=False)
    merchant_id = Column(String(36), ForeignKey("merchants.id"), nullable=False)
    
    action_type = Column(String(50), nullable=False) # PAYOUT, REFUND, MARKETING_SPEND, DEBT_RECOVERY, TREASURY_SWEEP
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    urgency = Column(String(20), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    priority = Column(Integer, default=3) # 1 (Highest) to 5 (Lowest)
    confidence = Column(Float, default=0.90) # Agent self-reported confidence
    reason = Column(Text, nullable=False)
    
    # FinGuard Intent classification results
    intent_label = Column(String(100), nullable=True)
    intent_purpose = Column(String(100), nullable=True)
    intent_confidence = Column(Float, default=0.0)
    
    # Status lifecycle: PROPOSED -> EVALUATING -> DECIDED -> AWAITING_APPROVAL -> APPROVED -> EXECUTED -> REJECTED -> BLOCKED
    status = Column(String(30), default="PROPOSED")
    final_decision = Column(String(20), nullable=True) # ALLOW, MODIFY, DELAY, ESCALATE, BLOCK
    
    raw_payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    agent = relationship("Agent", back_populates="proposals")
    merchant = relationship("Merchant", back_populates="proposals")
    conflict = relationship("ConflictRecord", back_populates="proposal", uselist=False)
    risk_assessment = relationship("RiskAssessmentRecord", back_populates="proposal", uselist=False)
    future_impact = relationship("FutureImpactRecord", back_populates="proposal", uselist=False)
    simulations = relationship("SimulationRecord", back_populates="proposal")
    decision_record = relationship("DecisionRecord", back_populates="proposal", uselist=False)
    human_approval = relationship("HumanApprovalRecord", back_populates="proposal", uselist=False)
    execution = relationship("ExecutionRecord", back_populates="proposal", uselist=False)
    audit = relationship("AuditRecord", back_populates="proposal", uselist=False)


class ConflictRecord(Base):
    __tablename__ = "conflict_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    
    conflict_detected = Column(Boolean, default=False)
    conflict_type = Column(String(50), default="NONE") # LIQUIDITY_RESERVE_THREAT, BUDGET_EXCEED, CONCURRENT_OUTFLOW
    severity = Column(String(20), default="LOW") # NONE, LOW, MEDIUM, HIGH, CRITICAL
    detected_agents = Column(JSON, default=list) # List of colliding agent details
    aggregate_outflow = Column(Float, default=0.0)
    available_cash = Column(Float, default=0.0)
    required_reserve = Column(Float, default=0.0)
    projected_shortfall = Column(Float, default=0.0)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("AgentProposal", back_populates="conflict")


class RiskAssessmentRecord(Base):
    __tablename__ = "risk_assessment_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    
    risk_score = Column(Float, nullable=False) # 0 to 100
    risk_level = Column(String(20), nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    risk_factors = Column(JSON, default=list) # List of factor strings
    model_confidence = Column(Float, default=0.95)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("AgentProposal", back_populates="risk_assessment")


class FutureImpactRecord(Base):
    __tablename__ = "future_impact_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    
    projected_cash = Column(Float, nullable=False)
    projected_reserve = Column(Float, nullable=False)
    reserve_shortfall = Column(Float, default=0.0)
    projected_liquidity_ratio = Column(Float, nullable=False)
    future_cash_pressure = Column(String(20), default="MODERATE") # LOW, MODERATE, HIGH, SEVERE
    expected_runway_days = Column(Integer, default=14)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("AgentProposal", back_populates="future_impact")


class SimulationRecord(Base):
    __tablename__ = "simulation_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"))
    
    scenario_id = Column(String(20), nullable=False) # SCENARIO_A, SCENARIO_B, SCENARIO_C, SCENARIO_D
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    immediate_outflow = Column(Float, nullable=False)
    deferred_outflow = Column(Float, default=0.0)
    remaining_cash = Column(Float, nullable=False)
    reserve_shortfall = Column(Float, default=0.0)
    liquidity_ratio = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    policy_compliant = Column(Boolean, default=True)
    is_recommended = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("AgentProposal", back_populates="simulations")


class DecisionRecord(Base):
    __tablename__ = "decision_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    
    decision = Column(String(20), nullable=False) # ALLOW, MODIFY, DELAY, ESCALATE, BLOCK
    decision_reason = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    modified_amount = Column(Float, nullable=True)
    deferred_amount = Column(Float, nullable=True)
    delay_hours = Column(Integer, default=0)
    risk_level = Column(String(20), nullable=False)
    confidence = Column(Float, default=0.95)
    supporting_factors = Column(JSON, default=list)
    requires_human_approval = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("AgentProposal", back_populates="decision_record")


class HumanApprovalRecord(Base):
    __tablename__ = "human_approval_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    
    human_reviewer = Column(String(100), default="Treasury Lead (You)")
    status = Column(String(20), default="PENDING") # PENDING, APPROVED, REJECTED, MODIFIED_APPROVED
    approved_amount = Column(Float, nullable=True)
    comments = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    proposal = relationship("AgentProposal", back_populates="human_approval")


class ExecutionRecord(Base):
    __tablename__ = "execution_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    
    status = Column(String(20), default="EXECUTED") # EXECUTED, FAILED, SIMULATED
    executed_amount = Column(Float, nullable=False)
    transaction_reference = Column(String(50), nullable=False)
    pre_execution_cash = Column(Float, nullable=False)
    post_execution_cash = Column(Float, nullable=False)
    pre_execution_reserve = Column(Float, nullable=False)
    post_execution_reserve = Column(Float, nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(JSON, default=dict)

    proposal = relationship("AgentProposal", back_populates="execution")


class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    proposal_id = Column(String(36), ForeignKey("agent_proposals.id"), unique=True)
    receipt_number = Column(String(50), unique=True, nullable=False) # e.g. FG-RCPT-2026-001
    action_hash = Column(String(64), nullable=False)
    
    agent_id = Column(String(50), nullable=False)
    agent_name = Column(String(100), nullable=False)
    original_amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=False)
    governance_decision = Column(String(20), nullable=False)
    risk_score = Column(Float, nullable=False)
    conflict_detected = Column(Boolean, default=False)
    conflict_summary = Column(Text, nullable=True)
    human_approver = Column(String(100), nullable=True)
    execution_status = Column(String(20), default="EXECUTED")
    decision_rationale = Column(Text, nullable=False)
    
    full_reasoning_payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship("AgentProposal", back_populates="audit")


class TransactionLedger(Base):
    __tablename__ = "transaction_ledger"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    merchant_id = Column(String(36), ForeignKey("merchants.id"))
    agent_id = Column(String(50), nullable=False)
    proposal_id = Column(String(36), nullable=True)
    transaction_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    reference = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
