import jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.core_models import User
from backend.models.pydentic_models import TokenData
from backend.settings import ALGORITHM, SECRET_KEY, pwd_context


async def confirm_user(db: AsyncSession, token: str) -> None:
    payload: dict = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
    )
    username_jwt = payload.get("sub")
    password_jwt = payload.get("password")
    email_jwt = payload.get("email")
    token_data = TokenData(username=username_jwt)
    if not token_data:
        raise HTTPException(
            status_code=400, detail="Неверный или просроченный токен"
        )
    user = User(username=username_jwt)
    user.password_hash = pwd_context.hash(password_jwt)
    user.email = email_jwt
    user.is_verified = True
    db.add(user)
    await db.commit()
    return {
        "response": "Регистрация прошла успешно!"
    }
