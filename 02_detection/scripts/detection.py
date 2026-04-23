from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

model = YOLO("../models/yolov8n.pt")
image_path = "../images/image.png"

results = model(image_path)
results[0].show()
print(len(results))
result = results[0]

for box in result.boxes:
    print("class:", box.cls)
    print("confidence:", float(box.conf[0]))
    print("bounding box:", box.xyxy[0])