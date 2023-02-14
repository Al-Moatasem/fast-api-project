from typing import List

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.api.login.auth import authorization_credentials
from src.db.pg_connect import db_session

from .repository import User as UserRepo
from .schemas import CreateUserRequest, CreateUserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])


# not used at the moment, as the endpoint has to receive a session object
def get_user_repo(db: Session = Depends(db_session)) -> UserRepo:
    return UserRepo(db)


@router.post(
    "/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED
)
def create_new_user(
    request: CreateUserRequest,
    db: Session = Depends(db_session),
):
    user_repo = UserRepo(db)
    user_data = user_repo.create(
        request.name, request.email, request.password, request.confirm_password
    )

    db.commit()
    db.refresh(user_data)

    return user_data


@router.get("/list_users", response_model=List[CreateUserResponse])
def get_all_users(
    request: Request,
    page_size: int = 100,
    offset: int = 0,
    db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):
    user_repo = UserRepo(db)
    users = user_repo.list(page_size, offset)
    return users


@router.get("/{user_id}", response_model=CreateUserResponse)
def get_user_by_id(
    request: Request,
    user_id: int,
    db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):
    user_repo = UserRepo(db)
    user = user_repo.get_by_id(user_id)
    if user:
        return user


@router.delete(
    "/delete/user_id/{user_id}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_by_id(
    # request: Request,
    user_id: int = None,
    db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):
    user_repo = UserRepo(db)
    user_repo.delete_by_id(user_id)
    db.commit()


@router.delete(
    "/delete/email/{email}",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_by_email(
    # request: Request,
    email: EmailStr = None,
    db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):
    # print(request.state.user_id)

    user_repo = UserRepo(db)
    user_repo.delete_by_email(email)
    db.commit()


# @router.put(
#     "/update/{user_id}",
# )
# def update_user(
#     user_id:int,
#     payload: UpdateUserRequest,
#     db: Session = Depends(db_session),
#     token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
# ):
#     ...
