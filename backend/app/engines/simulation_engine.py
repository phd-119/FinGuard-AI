"""
FinGuard AI - What-If Simulation Engine
Evaluates counterfactual execution scenarios before committing any financial resources.
Leverages the Optimization Engine to compute optimal liquidity splits.
"""

from typing import List
from app.models.models import AgentProposal, FinancialState
from app.schemas.schemas import ScenarioComparison, ConflictDetectionResult
from app.engines.optimization_engine import optimization_engine

class SimulationEngine:
    def simulate_scenarios(
        self,
        proposal: AgentProposal,
        state: FinancialState,
        conflict: ConflictDetectionResult
    ) -> List[ScenarioComparison]:
        
        amt = proposal.amount
        cash = state.cash_balance
        reserve = state.reserve_requirement
        
        # Optimize split envelope using Optimization Engine
        safe_immediate, deferred_b, delay_hours = optimization_engine.optimize_split_allocation(
            proposal=proposal,
            state=state,
            aggregate_pending_outflow=conflict.aggregate_outflow
        )

        scenarios = []

        # Scenario A: Full Immediate Execution
        rem_a = cash - amt
        shortfall_a = max(0.0, reserve - rem_a)
        ratio_a = max(0.0, round(rem_a / max(1.0, reserve), 3))
        risk_a = min(98.0, 45.0 + (shortfall_a / reserve) * 50.0) if shortfall_a > 0 else 25.0
        compliant_a = rem_a >= reserve

        scenarios.append(ScenarioComparison(
            scenario_id="SCENARIO_A",
            name="Execute Full Amount Immediately",
            description=f"Execute entire ₹{amt:,.2f} immediately without mitigation or rescheduling.",
            immediate_outflow=round(amt, 2),
            deferred_outflow=0.0,
            remaining_cash=round(rem_a, 2),
            reserve_shortfall=round(shortfall_a, 2),
            liquidity_ratio=ratio_a,
            risk_score=round(risk_a, 1),
            policy_compliant=compliant_a,
            is_recommended=compliant_a and not conflict.conflict_detected
        ))

        # Scenario B: Governed Split Execution (Recommended when reserve is threatened)
        rem_b = cash - safe_immediate
        shortfall_b = max(0.0, reserve - rem_b)
        ratio_b = max(0.0, round(rem_b / max(1.0, reserve), 3))
        risk_b = 32.0 if shortfall_b == 0 else 55.0
        compliant_b = rem_b >= reserve

        # Scenario B is recommended if A breaches reserve but B allows partial progress safely
        rec_b = (not compliant_a or conflict.conflict_detected) and safe_immediate > 0

        scenarios.append(ScenarioComparison(
            scenario_id="SCENARIO_B",
            name="Governed Split Execution",
            description=f"Execute ₹{safe_immediate:,.2f} now (within unreserved cash) and defer ₹{deferred_b:,.2f} until next settlement cycle (+{delay_hours}h).",
            immediate_outflow=round(safe_immediate, 2),
            deferred_outflow=round(deferred_b, 2),
            remaining_cash=round(rem_b, 2),
            reserve_shortfall=round(shortfall_b, 2),
            liquidity_ratio=ratio_b,
            risk_score=round(risk_b, 1),
            policy_compliant=compliant_b,
            is_recommended=rec_b
        ))

        # Scenario C: Reschedule / Delay Entire Amount
        rem_c = cash
        shortfall_c = 0.0
        ratio_c = round(cash / max(1.0, reserve), 3)
        risk_c = 22.0
        rec_c = not rec_b and not compliant_a and proposal.urgency in ["LOW", "MEDIUM"]

        scenarios.append(ScenarioComparison(
            scenario_id="SCENARIO_C",
            name=f"Reschedule Entire Amount (+{delay_hours}h)",
            description=f"Delay entire ₹{amt:,.2f} by {delay_hours} hours to align with expected incoming receivables of ₹{state.receivables:,.2f}.",
            immediate_outflow=0.0,
            deferred_outflow=round(amt, 2),
            remaining_cash=round(rem_c, 2),
            reserve_shortfall=0.0,
            liquidity_ratio=ratio_c,
            risk_score=round(risk_c, 1),
            policy_compliant=True,
            is_recommended=rec_c
        ))

        # Scenario D: Outright Block / Reject
        scenarios.append(ScenarioComparison(
            scenario_id="SCENARIO_D",
            name="Reject & Block Proposal",
            description="Completely cancel proposed action. No funds disbursed; zero liquidity impact.",
            immediate_outflow=0.0,
            deferred_outflow=0.0,
            remaining_cash=round(cash, 2),
            reserve_shortfall=0.0,
            liquidity_ratio=round(cash / max(1.0, reserve), 3),
            risk_score=0.0,
            policy_compliant=True,
            is_recommended=False
        ))

        # If none marked recommended yet, pick safest compliant
        if not any(s.is_recommended for s in scenarios):
            if compliant_a:
                scenarios[0].is_recommended = True
            elif compliant_b and safe_immediate > 0:
                scenarios[1].is_recommended = True
            else:
                scenarios[2].is_recommended = True

        return scenarios

simulation_engine = SimulationEngine()
