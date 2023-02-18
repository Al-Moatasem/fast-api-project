# Upload Image
## The business logic
### Uploading an Image
1. The user login to his account
2. open/navigate to "upload image" view
3. select an image for upload
   1. allowed extensions are `.png`,`.jpg`,`.jpeg`
   2. maximum file size is 2 Mb
      1. We may let the user select a file, then the application resize it to 2Mb, respecting image scale
4. upload the image into the file system
   1. uploads directory is `/uploaded_images/`
   2. images are partitioned by uploading date `/uploaded_images/yyyymmdd/`
   3. the file name will follow this pattern `basename__n.ext`, where `n` is an incremental value `001`, `002`, ..., this way we will handle duplicated file names with the same user, or different user


### Detecting objects
There are multiple approaches for the detection process
1. While the user selecting the image, he will choose the object(s) to detect, objects are predefined.
2. The user choose images to upload, then he navigate into "object detection" view
   1. a list of all images are displayed
   2. the user select images and objects to be detected
   3. we may add an option to filter the uploaded images to unprocessed images
   4. add pagination to this view

In addition to the above, the user could define the minimum confidence for detected objects

### Returned Objects
After the ML model detects the objects, we may let the user to choose how to receive the results
1. crop each detected objects
2. draw a rectangle around the object
plus these options, the detected objects will be listed as follows

   | object class | coordinates         | confidence |
   | ------------ | ------------------- | ---------- |
   | car          | x1 = ,y1=, x2=, y2= | 0.68       |
   | person       |                     |            |
   | car          |                     |            |
