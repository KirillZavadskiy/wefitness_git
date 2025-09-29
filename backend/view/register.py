from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.celery_app.celery_email.tasks import send_txt
from backend.models.core_models import User
from backend.models.pydantic_models import CreateUser
from backend.settings import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context
from backend.view.get_token import create_access_token


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
        },
        expires_delta=access_token_expires
    )
    user = User(username=user_data.username)
    user.password_hash = pwd_context.hash(user_data.password)
    user.email = user_data.email
    db.add(user)
    await db.commit()

    send_txt.delay(to_email=user_data.email, token=access_token)
    return {
        "response": "На почту отправлено сообщение для ее подтверждения."
    }
