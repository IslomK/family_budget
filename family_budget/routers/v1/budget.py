from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from family_budget.core.database import get_db_session
from family_budget.core.deps import get_current_user
from family_budget.models import Budget as BudgetModel
from family_budget.models import UserBudget
from family_budget.schemas.v1.budget import Budget, BudgetCreateRequest, SharedBudgetsList
from family_budget.schemas.v1.user import UserInDb
from family_budget.services.budget import create_budget

router = APIRouter()


@router.post(
    "/create",
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


@router.get(
    "/list",
    response_model=SharedBudgetsList,
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def get_budget_list(
    database: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    current_user: UserInDb = Depends(get_current_user),
):
    filters = [BudgetModel.created_by_id == current_user.id]
    if category:
        filters.append(BudgetModel.category.title == category)

    created_budgets = database.query(BudgetModel).filter(*filters).offset(skip).limit(limit).all()
    shared_budgets = database.query(UserBudget).filter(UserBudget.user_id == current_user.id).all()

    return SharedBudgetsList(
        created_budgets=created_budgets,
        shared_budgets=[shared_budget.budget for shared_budget in shared_budgets],
    )
