"""
FinGuard AI - Optimization Engine
Solves constrained liquidity allocation, optimal transaction splitting,
and multi-agent priority scheduling to maximize operational progress while
strictly preserving mandatory statutory reserves.
"""

from typing import List, Dict, Any, Tuple
from app.models.models import AgentProposal, FinancialState, Agent

class OptimizationEngine:
    def optimize_split_allocation(
        self,
        proposal: AgentProposal,
        state: FinancialState,
        aggregate_pending_outflow: float = 0.0
    ) -> Tuple[float, float, int]:
        """
        Computes the mathematical optimal split allocation for a proposal:
        (optimal_immediate_amount, deferred_amount, delay_hours)
        
        Constraints:
        1. Remaining cash after immediate disbursement >= state.reserve_requirement
        2. Immediate amount <= proposal.amount
        3. Prioritizes higher urgency and higher trust agents
        """
        available_cash = state.cash_balance
        reserve_requirement = state.reserve_requirement
        free_liquidity = max(0.0, available_cash - reserve_requirement)
        
        # If there is free liquidity, calculate optimal portion to allocate
        amount = proposal.amount
        
        if free_liquidity <= 0:
            # Zero free cash available: entire transaction must be delayed or blocked
            return 0.0, amount, 24
            
        if amount <= free_liquidity:
            # Entire amount fits comfortably in free cash
            return amount, 0.0, 0
            
        # Amount exceeds free liquidity -> allocate full free cash buffer or safe fraction
        # Leave a small safety buffer (e.g. 0% if free cash is clean buffer, or 100% of free cash)
        optimal_immediate = round(free_liquidity, 2)
        deferred_amount = round(amount - optimal_immediate, 2)
        
        # Delay hours depends on daily inflows/receivables schedule
        delay_hours = 24 if state.daily_inflows > 0 or state.receivables > 0 else 48
        
        return optimal_immediate, deferred_amount, delay_hours

    def optimize_multi_agent_allocations(
        self,
        proposals: List[Dict[str, Any]],
        available_cash: float,
        reserve_requirement: float
    ) -> List[Dict[str, Any]]:
        """
        Multi-agent combinatorial knapsack / greedy priority allocation optimizer.
        Allocates available free cash across competing autonomous agents
        weighted by: (Priority Score * Urgency Weight * Trust Score).
        """
        free_cash = max(0.0, available_cash - reserve_requirement)
        
        urgency_weights = {"CRITICAL": 4.0, "HIGH": 3.0, "MEDIUM": 2.0, "LOW": 1.0}
        
        # Score each proposal
        scored = []
        for p in proposals:
            u_weight = urgency_weights.get(p.get("urgency", "MEDIUM"), 2.0)
            priority = max(1, p.get("priority", 3))
            p_score = (6 - priority) * u_weight * (p.get("trust_score", 80.0) / 100.0)
            scored.append({
                **p,
                "allocation_score": p_score,
                "original_amount": p.get("amount", 0.0)
            })
            
        # Sort descending by allocation score
        scored.sort(key=lambda x: x["allocation_score"], reverse=True)
        
        remaining_free_cash = free_cash
        results = []
        
        for item in scored:
            amt = item["original_amount"]
            if remaining_free_cash >= amt:
                allocated = amt
                deferred = 0.0
                remaining_free_cash -= amt
                status = "FULL"
            elif remaining_free_cash > 0:
                allocated = remaining_free_cash
                deferred = amt - remaining_free_cash
                remaining_free_cash = 0.0
                status = "PARTIAL"
            else:
                allocated = 0.0
                deferred = amt
                status = "DEFERRED"
                
            results.append({
                **item,
                "allocated_immediate": round(allocated, 2),
                "deferred_amount": round(deferred, 2),
                "allocation_status": status
            })
            
        return results

optimization_engine = OptimizationEngine()
