

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext


class LoginPasswordHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, plain_password: str, confirm_password: str=None, hashed_password:str=None):
        self.plain_password = plain_password
        self.confirm_password = confirm_password
        self.hashed_password = hashed_password

    def match_password(self):
        if not self.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "No confirm password to validate, please enter the confirm password"
            )

        if self.plain_password != self.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Confirm password doesn't match"
            )
        else:
            return True

    def hash_password(self) -> str:
        hashed_password = self.pwd_context.hash(self.plain_password)
        return hashed_password

    def verify_password(self) -> bool:
        verified = self.pwd_context.verify(secret=self.plain_password, hash=self.hashed_password)
        return verified

