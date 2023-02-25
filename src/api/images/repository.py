from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .orm import UploadedImage as UploadedImageORM


class UploadedImage:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        user_id: int,
        file_name: str,
        file_path: str,
        hashed_value: str,
        size_bytes: int,
    ):
        # check if the file already exists
        uploaded_image = (
            self.session.query(UploadedImageORM)
            .filter(
                UploadedImageORM.user_id == user_id,
                UploadedImageORM.hash_value == hashed_value,
            )
            .first()
        )

        # this logic could be implemented on the DB side, by setting a unique constraint for user_id and hash_value
        if uploaded_image:
            existing_file_name = uploaded_image.file_name
            # existing_file_path = uploaded_image.file_path
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This file already uploaded, file name: {existing_file_name} ",
            )

        # Inserting a record in the table
        uploaded_image_data = UploadedImageORM(
            user_id=user_id,
            file_name=file_name,
            file_path=file_path,
            hash_value=hashed_value,
            size_bytes=size_bytes,
        )
        self.session.add(uploaded_image_data)

        return uploaded_image_data

