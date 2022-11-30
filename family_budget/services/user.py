from typing import List
import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from family_budget.core.exceptions import (
    BudgetNotExistsException,
    DuplicateBudgetException,
    InteralServerException,
)
from family_budget.models.budget import Budget, UserBudget
from family_budget.models.user import User as UserModel
from family_budget.schemas.v1.user import ShareUserBudgetRequest, UserCreateRequest, UserInDb


async def create_user(db: Session, request: UserCreateRequest, **extra_attrs) -> UserModel:
    data = {**jsonable_encoder(request, by_alias=False), **extra_attrs}
    data.pop("repeat_password")

    user_object = UserModel(**data)

    try:
        db.add(user_object)
        db.flush()
    except SQLAlchemyError as ex:
        logger.error(ex)
        raise InteralServerException()

    return user_object


async def share_user_budgets(
    db: Session, user_id: uuid.UUID, request: ShareUserBudgetRequest
) -> List[UserBudget]:
    budget = (
        db.query(Budget)
        .filter(Budget.created_by_id == user_id, Budget.id == request.budget_id)
        .first()
    )
    if not budget:
        logger.error(f"Budget not found. User - {user_id}, budget - {request.budget_id}")
        raise BudgetNotExistsException()

    shared_budgets = [
        UserBudget(user_id=shared_user_id, budget_id=request.budget_id, budget=budget)
        for shared_user_id in request.user_ids
    ]

    try:
        db.add_all(shared_budgets)
        db.flush()
    except IntegrityError as ex:
        logger.error(ex)
        raise DuplicateBudgetException()
    except SQLAlchemyError as ex:
        logger.error(ex)
        raise InteralServerException()

    return shared_budgets
