from fastapi import APIRouter

from family_budget.routers.v1 import auth, budget, healthcheck, operations, user

api_router = APIRouter(prefix="/v1")

api_router.include_router(healthcheck.router)
api_router.include_router(user.router, prefix="/users")
api_router.include_router(budget.router, prefix="/budgets")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(operations.router, prefix="/operations")
