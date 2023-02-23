import hashlib
import io
import os

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


async def upload_image(file: UploadFile):
    file_name = file.filename  # file_name.ext
    basename, file_extension = file_name.split(".")

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

    dest_file_path = str(UPLOAD_DIR / file_name)
    image.save(dest_file_path)

    return file_name, basename, file_extension, hashed_value
