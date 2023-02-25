from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.api.images.object_detect_onnx import get_detections, save_image
from src.api.login.auth import authorization_credentials
from src.configs.config import settings
from src.db.pg_connect import db_session

from .repository import UploadedImage
from .utils import delete_file, upload_image

router = APIRouter(prefix="/api/images", tags=["Images"])

UPLOAD_DIR = settings.uploaded_images_dir
SAVE_DETECTIONS_BBOX_DIR = settings.save_detections_bbox_dir


@router.post("/upload/", response_class=FileResponse)
async def upload_image_view(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):
    # 1) Upload the image
    (
        original_file_name,
        saved_file_name,
        dest_file_path,
        hashed_value,
        size_bytes,
    ) = await upload_image(file)

    # 2) Insert image metadata into the DB
    uploaded_image_repo = UploadedImage(db)
    user_id = request.state.user_id

    # if the file hash value already exists, delete the uploaded file
    try:
        uploaded_image_data = uploaded_image_repo.create(
            user_id=user_id,
            file_name=original_file_name,
            file_path=dest_file_path,
            hashed_value=hashed_value,
            size_bytes=size_bytes,
        )
        db.commit()
        db.refresh(uploaded_image_data)
    except HTTPException as e:
        delete_file(dest_file_path)
        raise e

    # 3) object detection
    image, detections = get_detections(
        input_image_path=dest_file_path,
        model=request.app.state.onnx_coco_model,
        model_class_list=request.app.state.onnx_coco_class_list,
        confidence_threshold=0.65,
        colors=request.app.state.bbox_colors,
        target_classes=["all"],
    )

    # Saving the image with bounding boxes surrounding the detected objects
    save_detections_bbox_file_path = str(SAVE_DETECTIONS_BBOX_DIR / saved_file_name)
    save_image(image, save_detections_bbox_file_path)

    return FileResponse(
        save_detections_bbox_file_path,
        headers={
            "hashed_value": hashed_value,
            "detections": str(detections),
            "file_name": original_file_name,
        },
    )
