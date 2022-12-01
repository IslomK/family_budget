from datetime import datetime
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from family_budget import models
from family_budget.core import const
from family_budget.core.config import get_settings
from family_budget.core.const import ALGORITHM
from family_budget.core.database import get_db_session
from family_budget.schemas.v1.auth import TokenPayload
from family_budget.schemas.v1.user import UserInDb

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/v1/auth/login", scheme_name="JWT")

settings = get_settings()


async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db_session)
) -> UserInDb:
    try:
        payload = jwt.decode(token, const.JWT_SECRET_KEY, algorithms=[ALGORITHM])

        data = TokenPayload(**payload)
        if datetime.fromtimestamp(data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = (
        db.query(models.User).filter(models.User.email == data.sub).first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserInDb.from_orm(user)
