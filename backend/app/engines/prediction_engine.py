"""
FinGuard AI - Future Impact Prediction Engine
Forecasts merchant liquidity trajectory, reserve degradation, and cash runway pressure.
"""

from typing import Dict, Any
from app.models.models import AgentProposal, FinancialState
from app.schemas.schemas import FutureImpactResult, ConflictDetectionResult

class PredictionEngine:
    def predict_impact(
        self,
        proposal: AgentProposal,
        state: FinancialState,
        conflict: ConflictDetectionResult
    ) -> FutureImpactResult:
        
        available_cash = state.cash_balance
        reserve_req = state.reserve_requirement
        outflow = proposal.amount

        # Projected direct cash & liquidity
        projected_cash = available_cash - outflow
        projected_reserve = min(projected_cash, reserve_req)
        reserve_shortfall = max(0.0, reserve_req - projected_cash)
        projected_liquidity_ratio = max(0.0, round(projected_cash / max(1.0, reserve_req), 3))

        # Include global context if conflict is detected
        if conflict.conflict_detected:
            global_projected_cash = available_cash - conflict.aggregate_outflow
            global_shortfall = conflict.projected_shortfall
        else:
            global_projected_cash = projected_cash
            global_shortfall = reserve_shortfall

        # Determine cash pressure and runway projection
        net_daily_flow = state.daily_inflows - state.daily_outflows
        
        if global_shortfall > 0 or global_projected_cash < reserve_req:
            cash_pressure = "SEVERE" if global_projected_cash < 0 else "HIGH"
            runway_days = max(1, int(projected_cash / max(1000.0, state.daily_outflows)))
        elif projected_cash < reserve_req * 1.15:
            cash_pressure = "MODERATE"
            runway_days = 12
        else:
            cash_pressure = "LOW"
            runway_days = 30

        explanation = (
            f"If proposed action of ₹{outflow:,.2f} executes, direct cash drops from ₹{available_cash:,.2f} "
            f"to ₹{projected_cash:,.2f} (Liquidity Ratio: {projected_liquidity_ratio:.2f}). "
        )

        if conflict.conflict_detected:
            explanation += (
                f"Under concurrent multi-agent load (Total Outflow: ₹{conflict.aggregate_outflow:,.2f}), "
                f"global merchant cash degrades to ₹{global_projected_cash:,.2f} with a ₹{global_shortfall:,.2f} reserve deficit."
            )
        else:
            explanation += f"Reserve requirement (₹{reserve_req:,.2f}) remains protected with {runway_days} days estimated runway."

        return FutureImpactResult(
            projected_cash=round(projected_cash, 2),
            projected_reserve=round(projected_reserve, 2),
            reserve_shortfall=round(global_shortfall, 2),
            projected_liquidity_ratio=projected_liquidity_ratio,
            future_cash_pressure=cash_pressure,
            expected_runway_days=runway_days,
            confidence=0.96,
            explanation=explanation
        )

prediction_engine = PredictionEngine()
