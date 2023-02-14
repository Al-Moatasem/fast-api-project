import os
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    env: str = Field(default="dev")
    debug: bool = Field(default=True)

    # FastAPI
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    app_title: str = Field(...)

    # PG Database
    pg_username: str = Field(...)
    pg_password: str = Field(...)
    pg_host: str = Field(...)
    pg_port: int = Field(default=5432)
    pg_database: str = Field(...)

    # Authentications
    jwt_secret_key: str = Field(...)
    jwt_algorithm: str = Field(...)  # RS256 uses Private/Public keys, HS256 uses Secret
    jwt_access_token_expire_minutes: int = 60 * 24  # 1 day

    @property
    def pg_connection_url(self) -> str:
        return f"postgresql://{self.pg_username}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"

    class Config:
        env_file = ".env"


class DevelopmentSettings(Settings):
    pass


class ProductionSettings(Settings):
    debug: bool = False


@lru_cache
def get_settings():
    """
    Load project settings and configuration, default environment is Development `dev`
    """
    env = os.getenv("env", default="dev")

    if env == "dev":
        return DevelopmentSettings()
    elif env == "prod":
        return ProductionSettings()
    else:
        return DevelopmentSettings()


settings = get_settings()
