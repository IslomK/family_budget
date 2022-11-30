from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel


class BudgetCategory(BaseModel):
    id: Optional[uuid.UUID] = None
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class BudgetCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    amount: int
    category_id: uuid.UUID
    created_by_id: uuid.UUID


class Budget(BudgetCreateRequest):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: BudgetCategory

    class Config:
        orm_mode = True


class SharedBudgetsList(BaseModel):
    created_budgets: Optional[List[Budget]]
    shared_budgets: Optional[List[Budget]]
