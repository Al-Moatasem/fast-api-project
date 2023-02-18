import io
from enum import Enum
from typing import List

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import StreamingResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from PIL import Image, ImageOps
from sqlalchemy.orm import Session

from src.api.login.auth import authorization_credentials
from src.configs.config import settings
from src.db.pg_connect import db_session

from .utils import upload_image

router = APIRouter(prefix="/api/images", tags=["Images"])

UPLOAD_DIR = settings.uploaded_images_dir


class ObjectClasses(Enum):
    car = "car"
    person = "person"


@router.post("/upload/")
async def upload_image_view(
    file: UploadFile = File(...),
    object_classes: List[ObjectClasses] = None,
    # db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):

    file_name, basename, file_extension, hashed_value = await upload_image(
        file
    )

    # file_image = open(str(dest_file_path), mode="rb")
    return [file_name, basename, file_extension, hashed_value]

