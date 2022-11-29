from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel


class BudgetCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    amount: int
    category: uuid.UUID
    created_by: uuid.UUID


class Budget(BudgetCreateRequest):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BudgetListResponse(BaseModel):
    data: List[Budget]
