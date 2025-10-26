import sqlite3
from edge_device import config

# --- Database Initialization ---
def init_db():
    """Creates the local database and table if they don't exist."""
    with sqlite3.connect(config.DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS local_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL,
            image_path TEXT NOT NULL UNIQUE,
            device_id TEXT NOT NULL,
            is_synced INTEGER DEFAULT 0 
        )
        """)
        conn.commit()

# --- Add a new detection ---
def add_detection(species, confidence, timestamp, image_path, device_id):
    """Adds a new detection to the local database."""
    with sqlite3.connect(config.DB_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO local_detections (species, confidence, timestamp, image_path, device_id) VALUES (?, ?, ?, ?, ?)",
                (species, confidence, timestamp, image_path, device_id)
            )
            conn.commit()
            print(f"Locally stored detection: {species} at {image_path}")
        except sqlite3.IntegrityError:
            print(f"Detection at {image_path} already exists in local DB.")
        except Exception as e:
            print(f"Error adding detection to local DB: {e}")

# --- Get unsynced detections ---
def get_unsynced_detections():
    """Fetches all detections that have not been synced (is_synced = 0)."""
    with sqlite3.connect(config.DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, species, confidence, timestamp, image_path, device_id FROM local_detections WHERE is_synced = 0")
        return cursor.fetchall()

# --- Mark a detection as synced ---
def mark_as_synced(detection_id):
    """Marks a specific detection as synced (is_synced = 1)."""
    with sqlite3.connect(config.DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE local_detections SET is_synced = 1 WHERE id = ?", (detection_id,))
        conn.commit()