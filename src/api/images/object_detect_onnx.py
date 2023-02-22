"""
Useful resources: https://learnopencv.com/object-detection-using-yolov5-and-opencv-dnn-in-c-and-python/

- DNN: Deep Neural Network
- `cv2.dnn.blobFromImage()`:
  - docs: https://docs.opencv.org/3.4/d6/d0f/group__dnn.html#ga29f34df9376379a603acd8df581ac8d7
  - Creates 4-dimensional blob from image. Optionally resizes and crops image from center, subtract mean values, scales values by scale factor, swap Blue and Red channels.

SCORE_THRESHOLD: To filter low probability class scores.
NMS_THRESHOLD: (Non-Maximum Suppression) To remove overlapping bounding boxes.
    The function NMSBoxes() takes a list of boxes, calculates IOU (Intersection Over Union), and decides to keep the boxes depending on the NMS_THRESHOLD
CONFIDENCE_THRESHOLD: Filters low probability detections.
"""


import cv2
import numpy as np

# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.4


def load_classes(classes_file_path: str):
    class_list = []
    with open(classes_file_path, "r") as f:
        class_list = [class_name.strip() for class_name in f.readlines()]
    return class_list


def load_trained_onnx_model(trained_model_path: str):
    """Load the DNN model"""
    print("Loading ONNX model - COCO dataset")
    model = cv2.dnn.readNet(trained_model_path)
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return model


def detect(image, model):
    """
    image: in NumPy array format
    Returns an `Numpy ndarray` (array of arrays) which will store results of the computation. The output will be used to get the bbox for classes.
    """
    # The image must be converted to a blob so the network/model can process it
    blob = cv2.dnn.blobFromImage(
        image=image,
        scalefactor=1 / 255.0,
        # should relate to the configuration used while training the model
        size=(INPUT_WIDTH, INPUT_HEIGHT),
        # swap OpenCV BGR into RGB
        swapRB=True,
        crop=False,
    )
    model.setInput(blob)
    # [from docs] Runs a forward pass to compute the net output, what does this mean???
    predications = model.forward()

    # predictions.shape  # a tuple of a 3-D array of size (1, num_rows, num_columns)
    return predications


def wrap_detection(image, predictions, class_list, confidence_threshold):
    # predictions.shape  # a tuple of a 3-D array of size (1, num_rows, num_columns)
    # predictions[0].shape  # (num_rows, num_columns)
    # rows: number of detections / bounding boxes
    # columns: x, y, w, h, confidence, class scores (depends on number of classes in the trained model)
    #   x, y: normalized center coordinates of the detected bounding box
    #   w, h: normalized width and height
    #   class score: ???

    results_dicts = []
    class_ids = []
    confidences = []
    boxes = []

    # original predication is 3-D array of size 1x row x column
    # It should be row x column
    predictions = predictions[0]

    rows = predictions.shape[0]

    image_width, image_height, _ = image.shape

    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    # Iterate through detections.
    for r in range(rows):
        row = predictions[r]
        confidence = row[4]

        # Discard bad detections and continue.
        if confidence >= confidence_threshold:
            classes_scores = row[5:]
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
            class_id = max_indx[1]

            #  Continue if the class score is above threshold.
            if classes_scores[class_id] > SCORE_THRESHOLD:
                detection = {}
                detection["class_id"] = class_id
                detection["class_name"] = class_list[class_id]
                detection["confidence"] = str(confidence)

                confidences.append(confidence)
                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                detection["left"] = left
                detection["top"] = top
                detection["width"] = width
                detection["height"] = height

                box = np.array([left, top, width, height])
                boxes.append(box)
                results_dicts.append(detection)

    # Perform non maximum suppression to eliminate redundant, overlapping boxes with lower confidences.
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, NMS_THRESHOLD)

    results = []

    for i in indexes:
        results.append(results_dicts[i])

    return results


def format_yolov5(image):
    row, col, _ = image.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = image
    return result


def crop_detection(image, left, top, width, height):
    # image[y:y+h, x:x+w]
    return image[top : top + height, left : left + width]


def draw_rectangle(
    image, left, top, width, height, class_name, color, add_label: bool = True
):
    if add_label:
        # Adding a label box above the bbox
        image = cv2.rectangle(image, (left, top - 20), (left + width, top), color, -1)
        # Adding label name
        image = cv2.putText(
            image,
            class_name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
        )

    # Drawing the box
    image = cv2.rectangle(image, (left, top), (left + width, height + top), color, 2)

    return image


def get_detections(
    input_image_path,
    model,
    model_class_list,
    confidence_threshold,
    colors,
    target_classes: list = ["all"],
):
    # read the image
    original_image = cv2.imread(input_image_path)
    # format the image (adjust the width and height)
    image = format_yolov5(original_image)
    # detect objects in the image
    predictions = detect(image=image, model=model)
    # process predictions and get the detections as a list of dicts
    detections = wrap_detection(
        image, predictions, model_class_list, confidence_threshold
    )

    # Filtering detections by class name
    target_classes_str = ",".join(target_classes)
    if target_classes is not None and target_classes_str == "all":
        # keep all detections
        pass
    else:
        detections = [
            detection
            for detection in detections
            if detection["class_name"] in target_classes_str
        ]

    for detection in detections:
        left = detection["left"]
        top = detection["top"]
        width = detection["width"]
        height = detection["height"]
        class_id = detection["class_id"]
        class_name = detection["class_name"]

        color = colors[int(class_id) % len(colors)]

        # cropped = crop_detection(image, left, top, width, height)
        image = draw_rectangle(
            original_image, left, top, width, height, class_name, color
        )

    return image, detections


def save_image(image, destination_path: str) -> None:
    cv2.imwrite(destination_path, image)
