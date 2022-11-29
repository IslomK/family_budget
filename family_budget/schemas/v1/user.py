from typing import List, Optional
import uuid

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    phone_number: str

    class Config:
        orm_mode = True


class ShareUserBudgetRequest(BaseModel):
    budget_id: uuid.UUID
    user_ids: List[uuid.UUID]
    message: str
    description: Optional[str]
