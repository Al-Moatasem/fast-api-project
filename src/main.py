from fastapi import FastAPI

from src.api.login.routers import router as login_router
from src.api.users.routers import router as users_router
from src.configs.config import settings
from src.middleware.auth import AuthorizeRequestMiddleware

app_debug = True if settings.env != "prod" else False
app = FastAPI(title=settings.app_title, debug=app_debug)

app.include_router(users_router)
app.include_router(login_router)
app.add_middleware(middleware_class=AuthorizeRequestMiddleware)


@app.get("/")
def home():
    return {"Hello": "Ahlan"}
