"""
FinGuard AI - Safe Alternative Engine
Generates constructive governed modifications (splits, delays, buffer protections)
leveraging the Optimization Engine so business operations proceed safely without reserve breaches.
"""

from app.models.models import AgentProposal, FinancialState
from app.schemas.schemas import SafeAlternativeResult, ScenarioComparison
from app.engines.optimization_engine import optimization_engine

class AlternativeEngine:
    def generate_alternative(
        self,
        proposal: AgentProposal,
        state: FinancialState,
        recommended_scenario: ScenarioComparison
    ) -> SafeAlternativeResult:
        
        amt = proposal.amount
        imm = recommended_scenario.immediate_outflow
        deferred = recommended_scenario.deferred_outflow
        
        if imm == amt:
            return SafeAlternativeResult(
                alternative_type="STANDARD_EXECUTION",
                immediate_amount=round(amt, 2),
                deferred_amount=0.0,
                delay_hours=0,
                recommended_action=f"Execute full amount ₹{amt:,.2f} immediately.",
                rationale="Financial state and risk parameters confirm proposal is fully within safe liquidity limits."
            )
        elif imm > 0 and deferred > 0:
            delay_hours = 24 if state.daily_inflows > 0 or state.receivables > 0 else 48
            return SafeAlternativeResult(
                alternative_type="SPLIT_TRANSACTION",
                immediate_amount=round(imm, 2),
                deferred_amount=round(deferred, 2),
                delay_hours=delay_hours,
                recommended_action=f"Execute ₹{imm:,.2f} now; defer remaining ₹{deferred:,.2f} by {delay_hours} hours.",
                rationale=(
                    f"Maintains mandatory minimum reserve of ₹{state.reserve_requirement:,.2f} intact "
                    f"while satisfying ₹{imm:,.2f} of the agent's urgent operational obligation."
                )
            )
        elif imm == 0 and deferred > 0:
            delay_hours = 24 if state.daily_inflows > 0 or state.receivables > 0 else 48
            return SafeAlternativeResult(
                alternative_type="RESCHEDULE_DELAY",
                immediate_amount=0.0,
                deferred_amount=round(deferred, 2),
                delay_hours=delay_hours,
                recommended_action=f"Reschedule entire ₹{amt:,.2f} to next clearing window (+{delay_hours}h).",
                rationale="Prevents immediate cash deficit until incoming receivables buffer liquidity."
            )
        else:
            return SafeAlternativeResult(
                alternative_type="BLOCK_AND_CANCEL",
                immediate_amount=0.0,
                deferred_amount=0.0,
                delay_hours=0,
                recommended_action="Block transaction execution entirely.",
                rationale="Proposal violates critical security or merchant solvency policies."
            )

alternative_engine = AlternativeEngine()
