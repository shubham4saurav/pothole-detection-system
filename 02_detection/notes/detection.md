## What is Object Detection?

- Detect objects and their location in an image
- Output: label + bounding box

## What is YOLO?

- Real-time object detection model
- Processes image in one pass

## Output of YOLO

- Class (object type)
- Confidence score
- Bounding box coordinates

## My Understanding

- YOLO sees the full image at once and predicts objects directly.
- It finds possible objects, gives each one a class and confidence, and draws a box.
- Then it removes duplicate/overlapping boxes and keeps the best ones.
- Final output gives:
  - `box.cls` -> class id (what object)
  - `box.conf` -> confidence (how sure model is)
  - `box.xyxy` -> bounding box coordinates (where object is)
