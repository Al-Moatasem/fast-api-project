import hashlib
import io
import os
import shutil
import uuid

from fastapi import File, HTTPException, UploadFile, status
from PIL import Image, ImageOps

from src.configs.config import settings

UPLOAD_DIR = settings.uploaded_images_dir


def get_file_size_bytes(file: str) -> int | None:
    size_bytes = os.stat(file).st_size
    return size_bytes


def hash_file_md5(file: str) -> str:
    hashed = hashlib.md5(open(file, "br").read()).hexdigest()
    return hashed


def delete_file(file: str) -> None:
    os.remove(file)


async def upload_image(file: UploadFile):
    original_file_name = file.filename  # file_name.ext
    file_extension = original_file_name.split(".")[-1]
    basename = original_file_name.split(".")[:-1]

    # validating the file extension
    if file_extension.lower() not in ["png", "jpeg", "jpg"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file format, please, upload an image with one of these formats: PNG/JPG/JPEG",
        )

    # read image as a stream of bytes
    image_stream = io.BytesIO(await file.read())

    # or
    # image_stream = io.BytesIO(file.file.read())
    # start the stream
    # image_stream.seek(0)  # start from the first byte

    # Validate if the file is an image
    try:
        image = Image.open(image_stream)

        # handle images that is taller than its width
        image = ImageOps.exif_transpose(image)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image"
        )

    # hashed_value = hashlib.md5(image_stream.getbuffer()).hexdigest()
    # the above line, and the below line, don't return the same hash value
    hashed_value = hashlib.md5(image.tobytes()).hexdigest()

    saved_file_name = f"{str(uuid.uuid1())}__{original_file_name}"
    dest_file_path = str(UPLOAD_DIR / saved_file_name)

    image.save(dest_file_path)

    size_bytes = get_file_size_bytes(dest_file_path)

    return original_file_name, saved_file_name, dest_file_path, hashed_value, size_bytes
