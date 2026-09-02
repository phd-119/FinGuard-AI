"""
FinGuard AI - Master Governance Pipeline Service
Coordinates the unbypassable 10-stage governance pipeline for all autonomous agent proposals.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import (
    AgentProposal, Agent, FinancialState, Policy,
    ConflictRecord, RiskAssessmentRecord, FutureImpactRecord,
    SimulationRecord, DecisionRecord, HumanApprovalRecord
)
from app.schemas.schemas import EvaluationPipelineResponse
from app.engines.action_gateway import action_gateway
from app.engines.intent_engine import intent_engine
from app.engines.policy_engine import policy_engine
from app.engines.conflict_engine import conflict_engine
from app.engines.prediction_engine import prediction_engine
from app.engines.risk_engine import risk_engine
from app.engines.trust_engine import trust_engine
from app.engines.simulation_engine import simulation_engine
from app.engines.optimization_engine import optimization_engine
from app.engines.alternative_engine import alternative_engine
from app.engines.decision_engine import decision_engine

class GovernancePipeline:
    def evaluate_proposal(self, db: Session, proposal_id: str) -> EvaluationPipelineResponse:
        proposal = db.query(AgentProposal).filter(AgentProposal.id == proposal_id).first()
        if not proposal:
            raise HTTPException(status_code=404, detail=f"Proposal ID '{proposal_id}' not found.")

        agent = db.query(Agent).filter(Agent.id == proposal.agent_id).first()
        state = db.query(FinancialState).filter(FinancialState.merchant_id == proposal.merchant_id).first()
        if not agent or not state:
            raise HTTPException(status_code=500, detail="Corrupted system state: Missing Agent or FinancialState entity.")

        proposal.status = "EVALUATING"
        db.commit()

        # Stage 1: Financial Intent Extraction & Classification
        intent_res = intent_engine.evaluate(proposal, agent)

        # Stage 2: Policy Compliance Checks
        policy_checks = policy_engine.evaluate(db, proposal, state, agent)
        violations = [p for p in policy_checks if not p.is_compliant]

        # Stage 3: Cross-Agent Conflict Detection (Global Multi-Agent Analysis)
        conflict_res = conflict_engine.detect_conflicts(db, proposal, state)

        # Stage 4: Future Impact & Liquidity Runway Prediction
        future_res = prediction_engine.predict_impact(proposal, state, conflict_res)

        # Stage 5: Agent Trust & Telemetry Profile
        trust_res = trust_engine.evaluate(db, agent)

        # Stage 6: Multi-Factor Risk Assessment
        risk_res = risk_engine.assess_risk(
            proposal=proposal,
            state=state,
            agent=agent,
            policy_checks=policy_checks,
            conflict=conflict_res,
            future_impact=future_res,
            trust=trust_res
        )

        # Stage 7: What-If Scenario Simulations (uses Optimization Engine)
        scenarios = simulation_engine.simulate_scenarios(proposal, state, conflict_res)
        recommended_scenario = next((s for s in scenarios if s.is_recommended), scenarios[0])

        # Stage 8: Safe Governed Alternative Synthesis (uses Optimization Engine)
        alternative_res = alternative_engine.generate_alternative(proposal, state, recommended_scenario)

        # Stage 9: Apex Decision Adjudication (ALLOW / MODIFY / DELAY / ESCALATE / BLOCK)
        decision_res = decision_engine.decide(
            proposal=proposal,
            state=state,
            agent=agent,
            policy_checks=policy_checks,
            conflict=conflict_res,
            future_impact=future_res,
            risk=risk_res,
            trust=trust_res,
            scenarios=scenarios,
            alternative=alternative_res
        )

        # --- Persist Analysis Records to Database ---
        # 1. Update Proposal State
        proposal.final_decision = decision_res.decision
        if decision_res.requires_human_approval:
            proposal.status = "AWAITING_APPROVAL"
        elif decision_res.decision == "BLOCK":
            proposal.status = "BLOCKED"
        elif decision_res.decision == "DELAY":
            proposal.status = "DELAYED"
        else:
            proposal.status = "DECIDED"

        # 2. Conflict Record (Upsert)
        conflict_rec = db.query(ConflictRecord).filter(ConflictRecord.proposal_id == proposal.id).first()
        if not conflict_rec:
            conflict_rec = ConflictRecord(proposal_id=proposal.id)
            db.add(conflict_rec)
        conflict_rec.conflict_detected = conflict_res.conflict_detected
        conflict_rec.conflict_type = conflict_res.conflict_type
        conflict_rec.severity = conflict_res.severity
        conflict_rec.detected_agents = conflict_res.detected_agents
        conflict_rec.aggregate_outflow = conflict_res.aggregate_outflow
        conflict_rec.available_cash = conflict_res.available_cash
        conflict_rec.required_reserve = conflict_res.required_reserve
        conflict_rec.projected_shortfall = conflict_res.projected_shortfall
        conflict_rec.explanation = conflict_res.explanation

        # 3. Risk Record (Upsert)
        risk_rec = db.query(RiskAssessmentRecord).filter(RiskAssessmentRecord.proposal_id == proposal.id).first()
        if not risk_rec:
            risk_rec = RiskAssessmentRecord(proposal_id=proposal.id)
            db.add(risk_rec)
        risk_rec.risk_score = risk_res.risk_score
        risk_rec.risk_level = risk_res.risk_level
        risk_rec.risk_factors = risk_res.risk_factors
        risk_rec.model_confidence = risk_res.model_confidence
        risk_rec.explanation = risk_res.explanation

        # 4. Future Impact Record (Upsert)
        future_rec = db.query(FutureImpactRecord).filter(FutureImpactRecord.proposal_id == proposal.id).first()
        if not future_rec:
            future_rec = FutureImpactRecord(proposal_id=proposal.id)
            db.add(future_rec)
        future_rec.projected_cash = future_res.projected_cash
        future_rec.projected_reserve = future_res.projected_reserve
        future_rec.reserve_shortfall = future_res.reserve_shortfall
        future_rec.projected_liquidity_ratio = future_res.projected_liquidity_ratio
        future_rec.future_cash_pressure = future_res.future_cash_pressure
        future_rec.expected_runway_days = future_res.expected_runway_days
        future_rec.explanation = future_res.explanation

        # 5. Simulation Records
        db.query(SimulationRecord).filter(SimulationRecord.proposal_id == proposal.id).delete()
        db.flush()
        for sc in scenarios:
            s_rec = SimulationRecord(
                proposal_id=proposal.id,
                scenario_id=sc.scenario_id,
                name=sc.name,
                description=sc.description,
                immediate_outflow=sc.immediate_outflow,
                deferred_outflow=sc.deferred_outflow,
                remaining_cash=sc.remaining_cash,
                reserve_shortfall=sc.reserve_shortfall,
                liquidity_ratio=sc.liquidity_ratio,
                risk_score=sc.risk_score,
                policy_compliant=sc.policy_compliant,
                is_recommended=sc.is_recommended
            )
            db.add(s_rec)

        # 6. Decision Record (Upsert)
        dec_rec = db.query(DecisionRecord).filter(DecisionRecord.proposal_id == proposal.id).first()
        if not dec_rec:
            dec_rec = DecisionRecord(proposal_id=proposal.id)
            db.add(dec_rec)
        dec_rec.decision = decision_res.decision
        dec_rec.decision_reason = decision_res.decision_reason
        dec_rec.recommended_action = decision_res.recommended_action
        dec_rec.modified_amount = decision_res.modified_amount
        dec_rec.deferred_amount = decision_res.deferred_amount
        dec_rec.delay_hours = decision_res.delay_hours
        dec_rec.risk_level = decision_res.risk_level
        dec_rec.confidence = decision_res.confidence
        dec_rec.supporting_factors = decision_res.supporting_factors
        dec_rec.requires_human_approval = decision_res.requires_human_approval

        # 7. Human Approval Record placeholder if human approval required
        if decision_res.requires_human_approval:
            existing_appr = db.query(HumanApprovalRecord).filter(HumanApprovalRecord.proposal_id == proposal.id).first()
            if not existing_appr:
                appr_rec = HumanApprovalRecord(
                    proposal_id=proposal.id,
                    human_reviewer="Treasury Lead (You)",
                    status="PENDING",
                    approved_amount=decision_res.modified_amount or proposal.amount,
                    comments=f"FinGuard evaluated decision as {decision_res.decision}. Awaiting human signoff."
                )
                db.add(appr_rec)

        # 8. Update trust outcome
        trust_engine.record_outcome(
            db=db,
            agent=agent,
            outcome=decision_res.decision,
            violation=(len(violations) > 0)
        )

        db.commit()

        return EvaluationPipelineResponse(
            proposal_id=proposal.id,
            agent_id=agent.id,
            agent_name=agent.name,
            original_amount=proposal.amount,
            action_type=proposal.action_type,
            status=proposal.status,
            timestamp=proposal.created_at,
            intent=intent_res,
            policy_checks=policy_checks,
            conflict=conflict_res,
            future_impact=future_res,
            risk_assessment=risk_res,
            trust_profile=trust_res,
            what_if_scenarios=scenarios,
            safe_alternative=alternative_res,
            decision=decision_res
        )

governance_pipeline = GovernancePipeline()
