from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from family_budget.core.database import get_db_session
from family_budget.core.deps import get_current_user
from family_budget.schemas.v1.budget import Budget, BudgetCreateRequest
from family_budget.services.budget import create_budget

router = APIRouter()


@router.post(
    "/budgets/",
    response_model=Budget,
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def create_budget_method(
    request: BudgetCreateRequest,
    database: Session = Depends(get_db_session),
):
    budgets = await create_budget(db=database, request=request)
    return budgets
