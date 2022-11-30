from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from family_budget import models
from family_budget.core.database import get_db_session
from family_budget.core.utils import create_access_token, create_refresh_token, verify_password
from family_budget.schemas.v1.auth import TokenSchema

router = APIRouter()


@router.post(
    "/login", summary="Create access and refresh tokens for user", response_model=TokenSchema
)
async def login(
    database: Session = Depends(get_db_session),
    request_form: OAuth2PasswordRequestForm = Depends(),
):
    user = database.query(models.User).filter_by(email=request_form.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    if not verify_password(request_form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
