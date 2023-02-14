from typing import Optional

from pydantic import BaseModel, EmailStr, SecretStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
