from typing import List

from fastapi import APIRouter, Depends, File, Request, UploadFile, status
from fastapi.responses import StreamingResponse
from fastapi.security.http import HTTPAuthorizationCredentials

from src.api.images.object_detect_onnx import get_detections, save_image
from src.api.login.auth import authorization_credentials
from src.configs.config import settings

from .utils import upload_image

router = APIRouter(prefix="/api/images", tags=["Images"])

UPLOAD_DIR = settings.uploaded_images_dir
SAVE_DETECTIONS_BBOX_DIR = settings.save_detections_bbox_dir


@router.post("/upload/", response_class=StreamingResponse)
async def upload_image_view(
    request: Request,
    file: UploadFile = File(...),
    # db: Session = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(authorization_credentials),
):
    file_name, basename, file_extension, hashed_value = await upload_image(file)

    uploaded_image_full_path = str(UPLOAD_DIR / file_name)

    image, detections = get_detections(
        input_image_path=uploaded_image_full_path,
        model=request.app.state.onnx_coco_model,
        model_class_list=request.app.state.onnx_coco_class_list,
        confidence_threshold=0.65,
        colors=request.app.state.bbox_colors,
        target_classes=["all"],
    )

    save_detections_bbox_file_path = str(SAVE_DETECTIONS_BBOX_DIR / file_name)
    save_image(image, save_detections_bbox_file_path)

    file_image = open(save_detections_bbox_file_path, mode="rb")
    return StreamingResponse(file_image, media_type="image/jpeg")
