from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db import User as UserModel
from src.db.pg_connect import db_session
from src.utils.password_handler import LoginPasswordHandler
from src.utils.token_handler import TokenHandler

from .schemas import LoginResponse

router = APIRouter(prefix="/api/login", tags=["Login"])

oauth2 = OAuth2PasswordBearer(tokenUrl=router.prefix)


@router.post("/", response_model=LoginResponse)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_session),
):
    user = db.query(UserModel).filter(UserModel.email == credentials.username).first()

    # check register user?
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )

    # validate the password
    LoginPasswordHandler(
        plain_password=credentials.password, hashed_password=user.password
    ).verify_password()

    # generate a token
    payload = {"sub": user.id, "role": user.role}
    token = TokenHandler.encode(payload=payload)

    return {"access_token": token, "token_type": "bearer"}
