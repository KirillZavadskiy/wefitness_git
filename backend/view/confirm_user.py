import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.core_models import User
from backend.models.pydentic_models import TokenData
from backend.settings import ALGORITHM, SECRET_KEY


async def confirm_user(db: AsyncSession, token: str) -> None:
    payload: dict = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
    )
    username_jwt = payload.get("sub")
    token_data = TokenData(username=username_jwt)
    if not token_data:
        raise HTTPException(
            status_code=400, detail="Неверный или просроченный токен"
        )
    user_jwt: User = await db.scalar(
        select(User).where(User.username == username_jwt)
    )
    user_jwt.is_verified = True
    await db.commit()
    return {
        "response": ("Почта подтверждена!"
                     "Вы можете вернуться на главную страницу.")
    }
