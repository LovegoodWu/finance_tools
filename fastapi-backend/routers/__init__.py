"""
Routers for API endpoints
"""

from fastapi import APIRouter

from .stock_routes import router as stock_router
from .strategy_routes import router as strategy_router
from .transaction_routes import router as transaction_router

__all__ = ["stock_router", "strategy_router", "transaction_router"]
