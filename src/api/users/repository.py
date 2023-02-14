from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.utils.password_handler import LoginPasswordHandler

from .orm import User as UserORM


class User:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[UserORM]:
        user = self.session.query(UserORM).filter(UserORM.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User ={user_id} doesn't exist",
            )
        return user

    def get_by_email(self, email: str) -> Optional[UserORM]:
        user = self.session.query(UserORM).filter(UserORM.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User ={email} doesn't exist",
            )
        return user

    def list(self, page_size: int = 100, offset: int = 0):
        page_size = 100 if page_size > 100 else page_size

        offset = offset * page_size

        users = self.session.query(UserORM).offset(offset).limit(page_size).all()
        return users

    def create(self, name, email, password, confirm_password) -> Optional[UserORM]:
        # check that password = confirm_password
        password_handler = LoginPasswordHandler(
            plain_password=password, confirm_password=confirm_password
        )

        password_handler.match_password()

        # check if the user already exist
        user_query = self.session.query(UserORM).filter(UserORM.email == email).first()

        if user_query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username or email already exists",
            )

        # hashing the password
        hashed_password = password_handler.hash_password()

        # user_data = UserModel({**request, 'password': hashed_password})
        user_data = UserORM(email=email, password=hashed_password, name=name)
        self.session.add(user_data)

        return user_data

    def delete_by_email(self, email: str = None):
        user_query = self.session.query(UserORM).filter(UserORM.email == email)
        user = user_query.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist, please check the input data.",
            )

        return user_query.delete(synchronize_session=False)

    def delete_by_id(self, user_id: int = None):
        user_query = self.session.query(UserORM).filter(UserORM.id == user_id)
        user = user_query.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist, please check the input data.",
            )

        return user_query.delete(synchronize_session=False)
