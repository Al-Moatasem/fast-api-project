import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    env: str = Field(default="dev")
    debug: bool = Field(default=True)

    base_dir: Path = Path(__file__).parent.parent.parent
    uploaded_images_dir: Path = base_dir / "uploaded_images"
    save_detections_bbox_dir:Path = base_dir / "detections_bbox"
    ml_dir: Path = base_dir / "ml"  # machine learning

    # FastAPI
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    app_title: str = Field(...)
    app_description: str = Field(...)

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

    # ML Models
    onnx_coco_model_path: str = Field(...)
    onnx_coco_classes_list_path: str = Field(...)

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

    Settings().uploaded_images_dir.mkdir(exist_ok=True, parents=True)
    Settings().save_detections_bbox_dir.mkdir(exist_ok=True, parents=True)

    env = os.getenv("env", default="dev")

    if env == "dev":
        return DevelopmentSettings()
    elif env == "prod":
        return ProductionSettings()
    else:
        return DevelopmentSettings()


settings = get_settings()
