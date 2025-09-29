from typing import Annotated

from annotated_types import MaxLen, MinLen
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing_extensions import Doc


class UserBase(BaseModel):
    id: int
    username: Annotated[str, MinLen(2), MaxLen(20)]


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(20)]
    password: Annotated[str, MinLen(2), MaxLen(20)]
    email: EmailStr


UserLogin = CreateUser

UserAuth = CreateUser


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ProgramSelect(BaseModel):
    template_name: str


class ProgressUpdate(BaseModel):
    start_value: float
    target_value: float
    current_value: float


class ChangeBodyProgramSelect(BaseModel):
    program_name: str


class Email(BaseModel):
    email: EmailStr


class OAuth2My(OAuth2PasswordRequestForm):
    email: Annotated[
        str,
        Form(),
        Doc(
                """
                `email` string. The OAuth2 spec requires the exact field name
                `email".
                """
        ),
    ]
