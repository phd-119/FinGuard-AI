"""
FinGuard AI - Master API Router Aggregator
"""

from fastapi import APIRouter
from app.api.routes import (
    merchants,
    agents,
    financial_state,
    policies,
    actions,
    conflicts,
    risk,
    simulations,
    approvals,
    audit,
    demo
)

api_router = APIRouter()

api_router.include_router(merchants.router)
api_router.include_router(agents.router)
api_router.include_router(financial_state.router)
api_router.include_router(policies.router)
api_router.include_router(actions.router)
api_router.include_router(conflicts.router)
api_router.include_router(risk.router)
api_router.include_router(simulations.router)
api_router.include_router(approvals.router)
api_router.include_router(audit.router)
api_router.include_router(demo.router)
