from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from family_budget.core.enums import OperationTypeEnum
from family_budget.models import Base
from family_budget.models.base import PostgresSQLUUID


class Operation(Base):
    title = Column(String(32))
    amount = Column(Integer, nullable=False)
    budget_id = Column(PostgresSQLUUID, ForeignKey("budget.id"), index=True)
    created_by_id = Column(PostgresSQLUUID, ForeignKey("user.id"), index=True)
    commentary = Column(Text, nullable=True)
    operation_type = Column(Enum(OperationTypeEnum))

    budget = relationship("Budget")
