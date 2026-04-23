from pathlib import Path

import matplotlib.pyplot as plt
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "runs" / "detect" / "train9" / "weights" / "best.pt"
IMAGE_PATH = BASE_DIR / "02_detection" / "images" / "pothole_3.webp"

model = YOLO(str(MODEL_PATH))

results = model(str(IMAGE_PATH))
annotated_image = results[0].plot(labels=False, conf=False)

plt.imshow(annotated_image[:, :, ::-1])
plt.axis("off")
plt.show()
