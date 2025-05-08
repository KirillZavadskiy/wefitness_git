from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


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
