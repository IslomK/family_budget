from typing import List, Optional
import uuid

from pydantic import BaseModel, validator

from family_budget.schemas.v1.budget import Budget


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str


class UserCreateRequest(UserBase):
    password: str
    repeat_password: str

    @validator("repeat_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class UserInDb(UserBase):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class ShareUserBudgetRequest(BaseModel):
    budget_id: uuid.UUID
    user_ids: List[uuid.UUID]
    message: str
    description: Optional[str]


class UserBudget(BaseModel):
    budget: Budget
    user: UserInDb

    class Config:
        orm_mode = True


class ShareUserBudgetResponse(BaseModel):
    shared_budget: List[UserBudget]
    created_by: uuid.UUID


a = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Njk3NzE4NjYsInN1YiI6ImlzYWV2QHNhaWQuc2FzYS5jb20ifQ.gTzU_gyIdzipS6tPIAwSNB-W4YHGxaC_ArgaDiHP0m0",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzAzNzQ4NzIsInN1YiI6ImlzYWV2QHNhaWQuc2FzYS5jb20ifQ.S9DrZvGqDnj_rmefRbPtcUNsLZIeDJPvKRzrKcEQ0AU",
}
