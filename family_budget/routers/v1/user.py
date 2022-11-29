import uuid

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from family_budget.core.config import Settings, get_settings
from family_budget.core.database import get_db_session
from family_budget.schemas.v1.budget import BudgetListResponse
from family_budget.schemas.v1.user import ShareUserBudgetRequest, User
from family_budget.services.budget import get_budget_by_user_id
from family_budget.services.user import get_user_by_id, share_user_budgets

router = APIRouter()


@router.get("/{user_id}", response_model=User, response_model_exclude_none=True)
async def get_user(
    user_id: uuid.UUID = Path(default=None, description="Id of the user to fetch"),
    database: Session = Depends(get_db_session),
    cfg: Settings = Depends(get_settings),
):
    user = await get_user_by_id(database, user_id)
    return user


@router.get(
    "/{user_id}/budgets", response_model=BudgetListResponse, response_model_exclude_none=True
)
async def get_budgets_by_user_id(
    user_id: uuid.UUID = Path(default=None, description="Id of the user to fetch"),
    database: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    budgets = await get_budget_by_user_id(database, user_id, skip, limit)
    return BudgetListResponse(data=budgets)


@router.post("/{user_id}/share-budget", response_model_exclude_none=True)
async def share_user_budgets_method(
    request: ShareUserBudgetRequest,
    user_id: uuid.UUID = Path(default=None, description="Id of the user to fetch"),
    database: Session = Depends(get_db_session),
):
    await share_user_budgets(db=database, user_id=user_id, request=request)
    return
