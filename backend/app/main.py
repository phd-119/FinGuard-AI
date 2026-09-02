"""
FinGuard AI - Master Application Entrypoint
Financial Governance Control Plane for Autonomous AI Agents
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.api.api import api_router
from app.services.seed_data import seed_database
from app.schemas.schemas import HealthResponse

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("finguard")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed baseline data
    logger.info("Initializing FinGuard AI database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_database(db)
        logger.info("FinGuard AI database successfully seeded with synthetic merchant & agent telemetry.")
    finally:
        db.close()
    
    yield
    logger.info("FinGuard AI shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"{settings.TAGLINE}\n\nSitting between autonomous AI agents and financial execution.",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API routes strictly under /api/v1 (SINGLE SOURCE OF TRUTH)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """
    Health check verifying FinGuard control plane is active and governing actions.
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        control_plane="FIN_GUARD_PROTECTED"
    )

@app.get("/", tags=["Root"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "status": "OPERATIONAL",
        "governance_status": "CONTROL_PLANE_ACTIVE",
        "documentation": "/docs",
        "api_v1": settings.API_V1_STR
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
