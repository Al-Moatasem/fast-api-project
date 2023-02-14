from fastapi import Request, status
from fastapi.responses import JSONResponse, Response
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
)
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.utils.token_handler import TokenHandler


# TODO: validation is required
class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request):
        access_token = request.cookies.get("access_token")

        token_payload = TokenHandler().decode(access_token)

        if token_payload is None:
            # anonymous user
            roles = ["anonymous"]
            return AuthCredentials(roles), UnauthenticatedUser()

        # TODO: validate the usage of `user_id`
        user_id = token_payload.get("sub")
        roles = ["authenticated"]
        # # SimpleUser class has a property called `is_authenticated` returns True
        return AuthCredentials(roles), SimpleUser(user_id)


EXCLUDE_URL_PATH = ["/", "/docs", "/openapi.json", "/api/users/", "/api/login/"]


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    # we can define the middleware also as follows in the `main.py`:
    # @app.middleware("http") # http is the scope, could be "websocket": for WebSocket connections, "lifespan": for ASGI lifespan messages.
    # and use the same logic here

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in EXCLUDE_URL_PATH:
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")

        # unauthorized user
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "details": "Missing access token",
                    "body": "Missing access token",
                },
            )

        try:
            # `auth_token` pattern > `Bearer <access_token>` or `Authorization <access_token>`
            auth_token = bearer_token.split(" ")[1].strip()

            # if it is invalid token, it will raise an exception
            token_payload = TokenHandler().decode(auth_token)

        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)},
            )
        else:
            request.state.user_id = token_payload["sub"]
            request.state.user_role = token_payload["role"]
        return await call_next(request)
