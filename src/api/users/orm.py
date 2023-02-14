from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql.expression import text

from src.db.mixin import MixinTimestamp
from src.db.pg_connect import Base


class User(Base, MixinTimestamp):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, server_default="user", nullable=False)
    is_active = Column(Boolean, server_default="FALSE", nullable=False)

    def dict(self):
        return {
            "user_id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
