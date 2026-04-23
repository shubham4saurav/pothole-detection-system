import json
import shutil
import uuid
from pathlib import Path
import datetime
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import create_table, get_connection
from ultralytics import YOLO
from validate import is_too_dark, is_valid_size, is_blurry

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "best.pt"
UPLOAD_FOLDER = BASE_DIR / "temp"
TRAINING_DATA_DIR = BASE_DIR / "training_data"
TRAINING_DATA_DIR.mkdir(exist_ok=True)
UPLOAD_FOLDER.mkdir(exist_ok=True)
create_table()
model = YOLO(str(MODEL_PATH))

app.mount("/images", StaticFiles(directory=TRAINING_DATA_DIR), name="images")




def is_duplicate_db(new_lat, new_lon, threshold=0.0001):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT lat, lon FROM reports")
    rows = cursor.fetchall()

    for lat, lon in rows:
        distance = ((new_lat - lat)**2 + (new_lon - lon)**2) ** 0.5
        if distance < threshold:
            conn.close()
            return True

    conn.close()
    return False


def save_report_db(report):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports (id, lat, lon, timestamp, status, verified, image_path, detections)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report["id"],
        report["location"]["lat"],
        report["location"]["lon"],
        report["timestamp"],
        report["status"],
        report.get("verified", False),
        report["image_path"],
        json.dumps(report.get("detections", []))
    ))

    conn.commit()
    conn.close()

@app.get("/")
def home():
    return {"message": "Pothole Detection API Running"}

@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    report_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_FOLDER / f"{file_id}.jpg"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Validation: image quality
    if is_blurry(file_path):
        file_path.unlink()
        return {"message": "Rejected: Image too blurry"}

    if is_too_dark(file_path):
        file_path.unlink()
        return {"message": "Rejected: Image too dark"}
    results = model(str(file_path))

    detections = []

    for box in results[0].boxes:
        detections.append({
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist()
        })

    # Apply validation filters
    valid_detections = []

    for d in detections:
        if d["confidence"] > 0.5 and is_valid_size(d["bbox"][0]):
            valid_detections.append(d)

    response = {
        "location": {
            "lat": latitude,
            "lon": longitude
        },
        "num_detections": len(valid_detections),
        "detections": valid_detections
    }
  

    if len(valid_detections) == 0:
        file_path.unlink()
        return {
            "message": "Rejected: No valid pothole detected",
            "report_saved": False
        }

    duplicate = is_duplicate_db(latitude, longitude)
    response["is_duplicate"] = duplicate

    if duplicate:
        response["report_saved"] = False
        response["message"] = "Duplicate pothole report detected for this location."
        return response

    image_path = TRAINING_DATA_DIR / f"{report_id}.jpg"
    shutil.copy(file_path, image_path)

    report = {
    "id": report_id,
    "location": {
        "lat": latitude,
        "lon": longitude
    },
    "timestamp": timestamp,
    "status": "reported",
    "verified": False,
    "image_path": str(image_path.name),
    "detections": valid_detections,
    "validated": True,
    "training_data": {
        "image": str(image_path),
        "detections": valid_detections
    }
   }
    save_report_db(report)
    response["report_saved"] = True
    response["message"] = "New pothole report saved."

    return response

@app.put("/update_status/{report_id}")
def update_status(report_id: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reports SET status = ? WHERE id = ?",
        (status, report_id),
    )
    conn.commit()
    conn.close()

    return {"message": "Status updated"}

@app.put("/verify/{report_id}")
def verify_report(report_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reports SET verified = ? WHERE id = ?",
        (True, report_id),
    )
    conn.commit()
    conn.close()

    return {"message": "Report verified"}

@app.get("/reports")
def get_reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()

    reports = []

    for row in rows:
        reports.append({
            "id": row[0],
            "location": {"lat": row[1], "lon": row[2]},
            "timestamp": row[3],
            "status": row[4],
            "verified": bool(row[5]),
            "image": row[6],
            "detections": json.loads(row[7]) if row[7] else []
        })

    conn.close()
    return reports
