# Pothole Detection System

This project is an end-to-end pothole reporting and monitoring system built with computer vision, FastAPI, SQLite, and a responsive Leaflet-based dashboard.

It covers the full pipeline:
- training a YOLO pothole detector
- validating uploaded road images
- detecting potholes from user-submitted images
- storing reports in SQLite
- serving saved evidence images through an API
- visualizing reports on an interactive map dashboard

## Project Overview

The system is organized into four main parts:

1. `01_basics`
- early image-processing practice scripts and notes

2. `02_detection`
- dataset preparation
- YOLO training scripts
- local model testing and detection utilities

3. `03_backend`
- FastAPI backend
- SQLite database integration
- image validation
- pothole report creation, verification, and status updates

4. `04_frontend`
- responsive dashboard UI
- map visualization with Leaflet
- image upload flow
- live pothole markers and popup previews

## Features

- YOLOv8-based pothole detection
- Image quality validation before saving a report
  - blur filtering
  - brightness filtering
  - bounding-box size filtering
- Duplicate report detection using nearby latitude/longitude matching
- Permanent storage of accepted report images
- SQLite-based report storage
- Static image serving through FastAPI
- Interactive frontend dashboard with:
  - map markers for all reports
  - report popups with image evidence
  - bounding boxes drawn on popup images
  - report statistics
  - recent activity panel
  - current-location map focus

## Tech Stack

- Python
- FastAPI
- SQLite
- Ultralytics YOLOv8
- OpenCV
- PyTorch
- Leaflet.js
- HTML, CSS, JavaScript

## Folder Structure

```text
.
├── 01_basics/
├── 02_detection/
│   ├── images/
│   ├── models/
│   ├── notes/
│   └── scripts/
├── 03_backend/
│   ├── model/
│   ├── temp/
│   ├── training_data/
│   ├── database.py
│   ├── database.db
│   ├── main.py
│   └── validate.py
├── 04_frontend/
│   ├── js/
│   ├── index.html
│   └── styles.css
├── dataset/
├── runs/
├── requirements.txt
└── Readme.md
```

## Backend Flow

When a user uploads an image:

1. The backend saves the uploaded image temporarily.
2. The image is validated for blur and darkness.
3. The YOLO model runs detection.
4. Low-confidence or too-small detections are filtered out.
5. The location is checked against existing reports to avoid duplicates.
6. Valid reports are saved:
   - image copied to `03_backend/training_data/`
   - report saved in SQLite
7. The frontend dashboard fetches reports and displays them on the map.

## Frontend Flow

The frontend dashboard:

- loads all reports from `GET /reports`
- renders them as map markers
- shows report details in popups
- displays the saved road image in the popup
- overlays bounding boxes directly on the popup image
- refreshes the dashboard after successful uploads

## API Endpoints

### `GET /`
Health check endpoint.

### `POST /detect`
Accepts:
- `file`
- `latitude`
- `longitude`

Runs validation and pothole detection, then saves a report if accepted.

### `GET /reports`
Returns all saved pothole reports from SQLite.

### `PUT /update_status/{report_id}`
Updates the report status, for example:
- `reported`
- `fixed`

### `PUT /verify/{report_id}`
Marks a report as verified.

### `GET /images/<filename>`
Serves saved report images from `03_backend/training_data`.

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Backend

From the project root:

```bash
cd 03_backend
uvicorn main:app --reload
```

Backend default URL:

```text
http://127.0.0.1:8000
```

## Running the Frontend

Open `04_frontend/index.html` in a browser.

For best results, keep the backend running first so the dashboard can fetch reports and images.

If your browser blocks local module loading from `file://`, serve the frontend with a simple local server:

```bash
cd 04_frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## Model Training

Training scripts are inside `02_detection/scripts`.

Main training entry point:

```bash
python 02_detection/scripts/train.py
```

## Notes

- Accepted report images are stored permanently in `03_backend/training_data/`
- The database file is `03_backend/database.db`
- Duplicate checking currently uses a simple distance threshold on latitude and longitude
- Bounding boxes shown in frontend popups come from saved detection metadata

## Future Improvements

- Add user authentication
- Add admin verification controls in the frontend
- Add filters for report status and verification
- Add pagination or clustering for large numbers of markers
- Improve duplicate checking with geospatial distance libraries
- Add report editing and deletion
- Add model retraining workflow from newly collected verified images

## Author

Pothole Detection System project for computer vision, backend API, and smart-city dashboard experimentation.
