from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from .routers import router

# get the login endpoint url
tokenUrl=router.prefix # .../api/login

# check the docs under authentication
oauth2 = OAuth2PasswordBearer(tokenUrl=tokenUrl)

# check the docs under authentication
authorization_credentials = HTTPBearer()



