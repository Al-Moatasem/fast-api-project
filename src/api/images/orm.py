from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from src.api.users.orm import User as UserModel
from src.db.mixin import MixinTimestamp
from src.db.pg_connect import Base


class UploadedImage(Base, MixinTimestamp):
    __tablename__ = "uploaded_images"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    hash_value = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="uploaded_images")
    def dict(self):
        return {
            "uploaded_image_id": self.id,
            "user_id": self.user_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "hash_value": self.hash_value,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ObjectClasses(Base, MixinTimestamp):
    __tablename__ = "object_classes"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # should be replaced with a relationship to a dedicated table
    ml_model_name = Column(String, nullable=False)
    ml_model_version = Column(String, nullable=False)
    ml_class_id = Column(Integer)
    ml_class_name = Column(String)


class DetectedObjects(Base, MixinTimestamp):
    __tablename__ = "detected_objects"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    uploaded_image_id = Column(Integer, ForeignKey(UploadedImage.id), nullable=False)
    object_class_id = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    left = Column(Integer, nullable=False)
    top = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
