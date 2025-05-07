from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: Annotated[str, MinLen(2), MaxLen(20)]


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(20)]
    password: Annotated[str, MinLen(2), MaxLen(20)]
    email: str


class UserLogin(CreateUser):
    pass


UserAuth = UserLogin


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
    email: str
