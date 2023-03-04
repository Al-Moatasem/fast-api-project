from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .orm import DetectedObjects as DetectedObjectORM
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

    def list(self, user_id: int, page_size: int = 100, offset: int = 0):
        page_size = 100 if page_size > 100 else page_size
        offset = offset * page_size

        images = (
            self.session.query(UploadedImageORM)
            .filter(UploadedImageORM.user_id == user_id)
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return images

    def get_by_id(self, image_id: int) -> Optional[UploadedImageORM]:
        uploaded_image = (
            self.session.query(UploadedImageORM)
            .filter(UploadedImageORM.id == image_id)
            .first()
        )
        if not uploaded_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Uploaded Image ={image_id} doesn't exist",
            )
        return uploaded_image

    def delete_by_id(self, image_id: int, user_id: int):
        image_query = self.session.query(UploadedImageORM).filter(
            UploadedImageORM.id == image_id, UploadedImageORM.user_id == user_id
        )
        uploaded_image = image_query.first()
        if not uploaded_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Selected image doesn't exist, please check the input data.",
            )

        return image_query.delete(synchronize_session=False)


class DetectedObjects:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        user_id: int,
        uploaded_image_id: int,
        object_class_id: int,
        confidence: float,
        left: int,
        top: int,
        width: int,
        height: int,
    ):
        # TODO: how to handle re-detecting objects on the image
        # ....

        # Inserting a record in the table
        detected_object_data = DetectedObjectORM(
            user_id=user_id,
            uploaded_image_id=uploaded_image_id,
            object_class_id=object_class_id,
            confidence=confidence,
            left=left,
            top=top,
            width=width,
            height=height,
        )
        self.session.add(detected_object_data)

        return detected_object_data

    def bulk_insert(self, data):
        # Inserting a record in the table
        if data:
            records = []
            for item in data:
                record = DetectedObjectORM(
                    user_id=item["user_id"],
                    uploaded_image_id=item["uploaded_image_id"],
                    object_class_id=item["class_id"],
                    confidence=item["confidence"],
                    left=item["left"],
                    top=item["top"],
                    width=item["width"],
                    height=item["height"],
                )
                records.append(record)

            self.session.add_all(records)

            return records

