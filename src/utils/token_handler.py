"""
The life cycle of a token:
1. The user passes credentials (login)
2. If passed credentials are valid, the application will get the user id
3. build the payload which includes a `sub` key that stores the user's id value
4. the payload is encoded to generate the token
5. the token could be added to the webpage cookies
6. decoding the token successfully means this is an authenticated user
7. A Middleware could be setup to decode the token and get the user id, then inject it to the request body.
   - this way, any received request, will have an identification to the user (if any) who sent it.
8. The token will be passed in each request header under the Authorization in the form of "Bearer <token>   
"""
from datetime import datetime, timedelta

import jwt
from fastapi.exceptions import HTTPException

from src.configs.config import settings

JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_access_token_expire_minutes


class TokenHandler:
    @staticmethod
    def encode(payload: dict) -> str:
        payload = {
            **payload,
            "exp": datetime.utcnow()
            + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        token = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(jwt=token, key=JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=JWT_SECRET_KEY,
                algorithms=JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, details="Invalid token")
