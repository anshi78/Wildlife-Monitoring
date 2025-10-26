from dotenv import load_dotenv
import os
import shutil
from datetime import datetime
from typing import List, Optional
from fastapi import (
    FastAPI, Depends, HTTPException, File, UploadFile, Form,
    Security, BackgroundTasks
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Local imports (Absolute, no dots)
import models
import database
from email_utils import send_email_alert

# --- Load environment variables & init DB ---
load_dotenv()
models.Base.metadata.create_all(bind=database.engine)

# --- FastAPI app & CORS ---
app = FastAPI(title="Wildlife Monitoring API")
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global state & Folder Setup ---
LATEST_IMAGE_PATH: Optional[str] = None
ALERT_RECIPIENT_EMAIL: Optional[str] = None
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

# --- Security ---
# This is the "Ghost-Fix": We hardcode the key to avoid all .env issues.
API_KEY = "MySuperSecretKey2025" 
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

# --- Dependency Functions ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Invalid or missing API Key")

# --- Pydantic Models ---
class Recipient(BaseModel):
    email: EmailStr

# --- API Endpoints ---
@app.post("/set-alert-recipient")
async def set_alert_recipient(recipient: Recipient, api_key: str = Depends(get_api_key)):
    global ALERT_RECIPIENT_EMAIL
    ALERT_RECIPIENT_EMAIL = recipient.email
    return {"message": "Alert recipient updated successfully."}

# Note the trailing slash on the URL
@app.post("/upload_detection/", response_model=models.DetectionOut, status_code=201)
async def upload_detection(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    species: str = Form(...),
    confidence: float = Form(...),
    timestamp: datetime = Form(...),
    device_id: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db), 
    api_key: str = Depends(get_api_key)
):
    global LATEST_IMAGE_PATH
    ext = os.path.splitext(file.filename)[1]
    filename = f"{device_id}_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    LATEST_IMAGE_PATH = file_path

    detection = models.Detection(
        species=species,
        confidence=confidence,
        timestamp=timestamp,
        device_id=device_id,
        location=location,
        image_path=file_path
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    if ALERT_RECIPIENT_EMAIL and species.lower() in ["leopard", "elephant"]:
        background_tasks.add_task(send_email_alert, ALERT_RECIPIENT_EMAIL, species, location, file_path)

    return detection

# Note the trailing slash on the URL
@app.get("/detections/", response_model=List[models.DetectionOut])
def get_detections(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return db.query(models.Detection).order_by(models.Detection.timestamp.desc()).all()

@app.get("/live-frame")
def get_live_frame():
    if LATEST_IMAGE_PATH and os.path.exists(LATEST_IMAGE_PATH):
        return FileResponse(LATEST_IMAGE_PATH, media_type="image/jpeg")
    return Response(status_code=404)

# Mount static files
app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_DIR), name="uploaded_images")