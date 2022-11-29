import uuid
from typing import List

from fastapi.logger import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from werkzeug.exceptions import InternalServerError

from family_budget.core.exceptions import BudgetNotExistsException, DuplicateBudgetException
from family_budget.models.budget import Budget, UserBudget
from family_budget.models.user import User as UserModel
from family_budget.schemas.v1.user import ShareUserBudgetRequest
from family_budget.schemas.v1.user import User as UserSchema


async def get_user_by_id(db: Session, user_id: uuid.UUID) -> UserSchema:
    return db.get(UserModel, user_id)


async def share_user_budgets(db: Session, user_id: uuid.UUID, request: ShareUserBudgetRequest) -> List[UserBudget]:
    budget = (
        db.query(Budget)
        .filter(Budget.created_by == user_id, Budget.id == request.budget_id)
        .first()
    )
    if not budget:
        logger.error(f"Budget not found. User - {user_id}, budget - {request.budget_id}")
        raise BudgetNotExistsException()

    shared_budgets = [
        UserBudget(user=shared_user_id, budget_id=request.budget_id)
        for shared_user_id in request.user_ids
    ]

    try:
        db.bulk_save_objects(shared_budgets)
    except IntegrityError as ex:
        logger.error(ex)
        raise DuplicateBudgetException()
    except SQLAlchemyError as ex:
        logger.error(ex)
        raise InternalServerError()

    return shared_budgets
