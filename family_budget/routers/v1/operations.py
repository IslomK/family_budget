from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from family_budget.core.database import get_db_session
from family_budget.core.deps import get_current_user
from family_budget.core.enums import OperationTypeEnum
from family_budget.core.exceptions import NotFoundException
from family_budget.models import Budget, Operation
from family_budget.schemas.v1.user import CreateOperationRequest, UserInDb
from family_budget.services.operation import create_operation

router = APIRouter()


@router.post(
    "/create-operation",
    dependencies=[Depends(get_current_user)],
    response_model_exclude_none=True,
)
async def get_user_incomes(
    request: CreateOperationRequest,
    current_user: UserInDb = Depends(get_current_user),
    database: Session = Depends(get_db_session),
):
    request.created_by_id = current_user.id

    budget = database.get(Budget, request.budget_id)

    if not budget:
        raise NotFoundException()

    operation = await create_operation(db=database, request=request, budget=budget)
    return operation


@router.get("/expenses", dependencies=[Depends(get_current_user)])
async def get_user_expenses(
    database: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
):
    filters = [Operation.operation_type == OperationTypeEnum.OUTCOMES]
    if category:
        filters.append(Operation.budget.category.title == category)

    operations = database.query(Operation).filter(*filters).offset(skip).limit(limit).all()
    if not operations:
        raise NotFoundException()

    return operations


@router.get(
    "/incomes",
    dependencies=[Depends(get_current_user)],
    response_model_exclude_none=True,
)
async def get_user_incomes(
    current_user: UserInDb = Depends(get_current_user),
    database: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
):
    filters = [
        Operation.operation_type == OperationTypeEnum.INCOMES,
        Operation.created_by_id == current_user.id,
    ]
    if category:
        filters.append(Operation.budget.category.title == category)

    operations = database.query(Operation).filter(*filters).offset(skip).limit(limit).all()
    if not operations:
        raise NotFoundException()
    return operations

