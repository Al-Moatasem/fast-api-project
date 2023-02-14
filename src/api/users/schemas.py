from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr, constr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: SecretStr
    role: Optional[str] = "user"
    is_active: Optional[bool] = False


class CreateUserRequest(BaseModel):
    name: constr(
        strip_whitespace=True, regex="^[0-9a-zA-Z-_ ]+$", max_length=25, min_length=3
    )
    email: EmailStr
    password: str
    confirm_password: str


class CreateUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True

        # We could inherit from `User` schema, and then exclude fields
        # fields = {
        #     'password': {'exclude': True},
        #     }


class DeleteUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None


class UpdateUserRequest(BaseModel):
    ...
