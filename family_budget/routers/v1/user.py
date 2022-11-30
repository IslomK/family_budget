from fastapi import APIRouter, Depends
from fastapi.logger import logger
from fastapi_pagination import Page, paginate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from family_budget.core.database import get_db_session
from family_budget.core.deps import get_current_user
from family_budget.core.exceptions import EmailDuplicateException, NotFoundException
from family_budget.models import User
from family_budget.models import Budget as BudgetModel

from family_budget.schemas.v1.budget import Budget
from family_budget.schemas.v1.user import (
    ShareUserBudgetRequest,
    ShareUserBudgetResponse,
    UserBudget,
    UserCreateRequest,
    UserInDb,
)
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
    "/details",
    response_model=UserInDb,
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def get_user(
    database: Session = Depends(get_db_session),
    current_user: UserInDb = Depends(get_current_user),
):
    try:
        user = database.get(User, current_user.id)
    except SQLAlchemyError as ex:
        logger.error(ex)
        raise NotFoundException()
    return user


@router.get(
    "/budgets",
    response_model=Page[Budget],
    response_model_exclude_none=True,
    dependencies=[Depends(get_current_user)],
)
async def get_budgets_by_user_id(
    database: Session = Depends(get_db_session),
    current_user: UserInDb = Depends(get_current_user),
):
    query = database.query(BudgetModel).filter(BudgetModel.created_by_id == current_user.id)

    return paginate(query.all())


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
