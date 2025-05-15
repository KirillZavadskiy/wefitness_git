from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.core_models import User
from models.pydentic_models import UserLogin
from settings import pwd_context


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(db: AsyncSession, username: UserLogin):
    user: User = await db.scalar(
        select(User).where(User.username == username)
    )
    return user


async def authenticate_user(
        db: AsyncSession,
        username,
        password,
        email
):
    user: User = await get_user(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username.")
    if not await verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect pass.")
    if not user.email == email:
        raise HTTPException(status_code=400, detail="Incorrect email.")

    return user
