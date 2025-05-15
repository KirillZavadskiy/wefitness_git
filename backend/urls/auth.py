from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db_connect import get_db
from models.core_models import User
from models.pydentic_models import (CreateUser, OAuth2My, Token,
                                    UserLogin)
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from view.authenticate import authenticate_user
from view.confirm_user import confirm_user
from view.get_token import create_access_token
from view.register import register

auth_router = APIRouter(tags=["Auth"])


@auth_router.get("/verify-email/")
async def successful_register(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    return await confirm_user(token=token, db=db)


@auth_router.post(
        "/register/",
        status_code=201
)
async def register_user(
    user_data: CreateUser,
    db: AsyncSession = Depends(get_db)
):
    return await register(db, user_data)


@auth_router.post("/login/")
async def login_for_access_token(
    form_data: Annotated[OAuth2My, Depends(UserLogin)],
    db: AsyncSession = Depends(get_db),
):
    user: User = await authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password,
        email=form_data.email
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
