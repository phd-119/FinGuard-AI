"""
FinGuard AI - System Configuration
"""

import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinGuard AI"
    TAGLINE: str = "Financial Governance Control Plane for Autonomous AI Agents"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    API_V1_STR: str = "/api/v1"  # Standard /api/v1 route namespace
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'finguard.db')}")
    
    # ML Models Directory
    ML_MODELS_DIR: str = os.getenv("ML_MODELS_DIR", os.path.join(PROJECT_ROOT, "ml", "models"))
    
    # Governance Defaults
    DEFAULT_MINIMUM_RESERVE: float = 500000.0  # ₹5,00,000
    DEFAULT_MERCHANT_CASH: float = 600000.0    # ₹6,00,000
    MAX_SINGLE_TRANSACTION_LIMIT: float = 500000.0 # ₹5,00,000
    DAILY_PAYOUT_LIMIT: float = 800000.0
    DAILY_REFUND_LIMIT: float = 200000.0
    DAILY_MARKETING_LIMIT: float = 300000.0
    HUMAN_APPROVAL_RISK_THRESHOLD: float = 65.0
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    class Config:
        case_sensitive = True

settings = Settings()
