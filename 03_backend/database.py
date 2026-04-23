import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id TEXT PRIMARY KEY,
        lat REAL,
        lon REAL,
        timestamp TEXT,
        status TEXT,
        verified BOOLEAN,
        image_path TEXT,
        detections TEXT
    )
    """)

    cursor.execute("PRAGMA table_info(reports)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if "detections" not in existing_columns:
        cursor.execute("ALTER TABLE reports ADD COLUMN detections TEXT")

    conn.commit()
    conn.close()
