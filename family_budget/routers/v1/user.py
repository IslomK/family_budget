import uuid

from fastapi import APIRouter, Depends, Path
from fastapi.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from family_budget.core.database import get_db_session
from family_budget.core.deps import get_current_user
from family_budget.core.exceptions import EmailDuplicateException, NotFoundException
from family_budget.models import User
from family_budget.schemas.v1.budget import BudgetListResponse
from family_budget.schemas.v1.user import (
    ShareUserBudgetRequest,
    ShareUserBudgetResponse,
    UserBudget,
    UserCreateRequest,
    UserInDb,
)
from family_budget.services.budget import get_budget_by_user_id
from family_budget.services.user import create_user, share_user_budgets

router = APIRouter()


@router.post("/create", response_model=UserInDb, response_model_exclude_none=True)
async def create_user_method(
    request: UserCreateRequest,
    database: Session = Depends(get_db_session),
):

    if database.query(User).filter_by(email=request.email).first() is not None:
        raise EmailDuplicateException()

    user = await create_user(database, request)
    return UserInDb.from_orm(user)


@router.get(
    "/{user_id}",
    response_model=UserInDb,
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def get_user(
    user_id: uuid.UUID = Path(default=None, description="Id of the user to fetch"),
    database: Session = Depends(get_db_session),
):
    try:
        user = database.get(User, user_id)
    except SQLAlchemyError as ex:
        logger.error(ex)
        raise NotFoundException()
    return user


@router.get(
    "/{user_id}/budgets",
    response_model=BudgetListResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def get_budgets_by_user_id(
    user_id: uuid.UUID = Path(default=None, description="Id of the user to fetch"),
    database: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    budgets = await get_budget_by_user_id(database, user_id, skip, limit)
    return BudgetListResponse(data=budgets)


@router.post(
    "/share-budget",
    response_model=ShareUserBudgetResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def share_user_budgets_method(
    request: ShareUserBudgetRequest,
    database: Session = Depends(get_db_session),
    current_user: UserInDb = Depends(get_current_user),
):
    shared_budgets = [
        UserBudget.from_orm(user_budget)
        for user_budget in await share_user_budgets(
            db=database, user_id=current_user.id, request=request
        )
    ]

    return ShareUserBudgetResponse(shared_budget=shared_budgets, created_by=current_user.id)
