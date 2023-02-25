from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer, String
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
            "original_file_name": self.original_file_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
