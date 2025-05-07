from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from settings import ALGORITHM, SECRET_KEY
from db_connect import get_db
from models.pydentic_models import TokenData
from view.authenticate import get_user

http_bearer = HTTPBearer()


async def get_current_user(
        token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        db: AsyncSession = Depends(get_db)
):
    access_token = token.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload: dict = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
