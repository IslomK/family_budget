from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from family_budget.core.enums import OperationTypeEnum
from family_budget.core.exceptions import InteralServerException
from family_budget.models import Budget, Operation
from family_budget.schemas.v1.user import CreateOperationRequest


async def create_operation(
    db: Session, request: CreateOperationRequest, budget: Budget, **extra_attrs
) -> Operation:
    data = {**jsonable_encoder(request, by_alias=False), **extra_attrs}

    # update the balance regarding to the operation type
    if request.operation_type == OperationTypeEnum.INCOMES:
        budget.amount += request.amount
    else:
        budget.amount -= request.amount

    operation_obj = Operation(**data)

    try:
        db.add(operation_obj)
        db.flush()
    except SQLAlchemyError as ex:
        logger.error(ex)
        raise InteralServerException()

    return operation_obj
