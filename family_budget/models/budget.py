from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from family_budget.models.base import Base, PostgresSQLUUID


class BudgetCategory(Base):
    title = Column(String(32))
    description = Column(Text)


class Budget(Base):
    title = Column(String(32))
    description = Column(Text)
    amount = Column(Integer, nullable=False)
    category_id = Column(PostgresSQLUUID, ForeignKey("budgetcategory.id"), index=True)
    created_by_id = Column(PostgresSQLUUID, ForeignKey("user.id"), index=True)

    category = relationship("BudgetCategory", backref="category_budgets")
    created_by = relationship("User", backref="owner_budgets")


class UserBudget(Base):
    title = Column(String(32))
    budget_id = Column(PostgresSQLUUID, ForeignKey("budget.id"), primary_key=True, index=True)
    user_id = Column(PostgresSQLUUID, ForeignKey("user.id"), primary_key=True, index=True)

    budget = relationship("Budget")
    user = relationship("User")
