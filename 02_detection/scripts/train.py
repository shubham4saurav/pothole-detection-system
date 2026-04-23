from pathlib import Path

from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "yolov8n.pt"
DATA_PATH = BASE_DIR / "dataset" / "potholes" / "data.yaml"

model = YOLO(str(MODEL_PATH))
model.train(
    data=str(DATA_PATH),
    epochs=50,
    imgsz=640,
)
