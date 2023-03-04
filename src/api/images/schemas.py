from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class UploadedImage(BaseModel):
    id: int
    user_id: int
    file_path: Path
    size_bytes: int
    file_name: str
    hash_value: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]


class UploadImageResponse(UploadedImage):
    class Config:
        orm_mode = True
