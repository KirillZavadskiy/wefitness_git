from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from celery_email.tasks import send_txt
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from models.core_models import User
from models.pydentic_models import CreateUser
from view.get_token import create_access_token


async def register(db: AsyncSession, user_data: CreateUser):
    user_is: User = await db.scalar(
        select(User).where(User.username == user_data.username)
    )
    if user_is:
        raise HTTPException(status_code=400, detail="User already exist.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={
            "sub": user_data.username,
            "password": user_data.password,
            "email": user_data.email
        },
        expires_delta=access_token_expires
    )
    send_txt.delay(to_email=user_data.email, token=access_token)
    return {
        "response": "На почту отправлено сообщение."
    }
