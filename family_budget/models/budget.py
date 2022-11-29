from sqlalchemy import Column, ForeignKey, Integer, String, Text

from family_budget.models.base import Base, PostgresSQLUUID


class BudgetCategory(Base):
    title = Column(String(32))
    description = Column(Text)


class Budget(Base):
    title = Column(String(32))
    description = Column(Text)
    amount = Column(Integer, nullable=False)
    category = Column(PostgresSQLUUID, ForeignKey("budgetcategory.id"), index=True)
    created_by = Column(PostgresSQLUUID, ForeignKey("user.id"), index=True)


class UserBudget(Base):
    budget_id = Column(PostgresSQLUUID, ForeignKey("budget.id"), primary_key=True, index=True)
    user = Column(PostgresSQLUUID, ForeignKey("user.id"), primary_key=True, index=True)
