from fastapi import FastAPI

from src.api.images.object_detect_onnx import load_classes, load_trained_onnx_model
from src.api.images.routers import router as images_router
from src.api.login.routers import router as login_router
from src.api.users.routers import router as users_router
from src.configs.config import settings
from src.middleware.auth import AuthorizeRequestMiddleware

app_debug = True if settings.env != "prod" else False
app = FastAPI(title=settings.app_title, debug=app_debug)
app.description = settings.app_description
# hide Schemas section in the `/docs`
app.swagger_ui_parameters = {"defaultModelsExpandDepth": -1}


app.include_router(users_router)
app.include_router(login_router)
app.include_router(images_router)
app.add_middleware(middleware_class=AuthorizeRequestMiddleware)


ML_DIR = settings.ml_dir
ONNX_COCO_CLASSES_LIST_PATH = str(ML_DIR / settings.onnx_coco_classes_list_path)
ONNX_COCO_MODEL_PATH = str(ML_DIR / settings.onnx_coco_model_path)


@app.on_event("startup")
def on_startup():
    onnx_coco_class_list = load_classes(ONNX_COCO_CLASSES_LIST_PATH)
    onnx_coco_model = load_trained_onnx_model(ONNX_COCO_MODEL_PATH)
    # Light blue / Green / Yellow / Blue
    COLORS = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]

    # Adding the model to the application
    # call it request.app.state. ....
    # TODO: consider creating a class
    app.state.ml_onnx_coco = {
        "name": "onnx_coco",
        "version": "1.0.0",
        "class_list": onnx_coco_class_list,
        "model": onnx_coco_model,
        "minimum_confidence": 0.4,  # use the maximum value of minimum_confidence and passed threshold from the user
    }
    app.state.bbox_colors = COLORS


@app.get("/")
def home():
    return {"Hello": "Ahlan"}
