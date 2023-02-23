# Object Detection

I have used [Yolov5](https://github.com/ultralytics/yolov5) for object detection, they are providing a model that can detect 80 object types (classes), Yolov5 depends on PyTorch for training the model, and for the detection part.

The PyTorch library is quite big (~810 MB), the library is required for training models, but for detection we can depend on other libraries such as OpenCV and ONNX, or Paddle (not test yet)

**OpenCV & ONNX**
1. export the trained model to `onnx` format
   ```bash
   python export.py --weights yolov5s.pt --include onnx --opset 12
   ```
   - `opset` opset version for the ONNX, if we didn't specif this option, we will get the following error while detection
     ```
     [ERROR:0@0.092] global onnx_importer.cpp:1054 cv::dnn::dnn4_v20221220::ONNXImporter::handleNode DNN/ONNX: 
     ERROR during processing node with 2 inputs and 3 outputs: [Split]:(onnx_node!/model.24/Split) from domain='ai.onnx'
     Traceback (most recent call last):
       File "...\detect_with....py", line 30, in <module>    
         net = cv2.dnn.readNet(onnx_model_path)
     cv2.error: OpenCV(4.7.0) D:\a\opencv-python\opencv-python\opencv\modules\dnn\src\onnx\onnx_importer.cpp:1073: error: (-2:Unspecified error) in function 'cv::dnn::dnn4_v20221220::ONNXImporter::handleNode'
     > Node [Split@ai.onnx]:(onnx_node!/model.24/Split) parse error: OpenCV(4.7.0) D:\a\opencv-python\opencv-python\opencv\modules\dnn\src\layers\slice_layer.cpp:274: error: (-215:Assertion failed) splits > 0 && inpShape[axis_rw] % splits == 0 in function 'cv::dnn::SliceLayerImpl::getMemoryShapes'
     >     
     ```
2. Install the necessary packages
   ```bash
   pip install opencv-python==4.7.0.68
   pip install onnx==1.13.0
   pip install numpy pandas
   ```
3. Follow this guide for detecting objects ([Medium](https://medium.com/mlearning-ai/detecting-objects-with-yolov5-opencv-python-and-c-c7cf13d1483c) / [GitHub](https://github.com/doleron/yolov5-opencv-cpp-python/blob/main/python/yolo.py))   
4. Other resources
   1. [How to use Yolo v5 without pytorch](https://github.com/ultralytics/yolov5/issues/10028)
