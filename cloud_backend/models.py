from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from pydantic import BaseModel as PydanticBaseModel # Rename to avoid conflict
from datetime import datetime
from database import Base # Corrected: Absolute import

# SQLAlchemy Model (for the database table)
class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, index=True)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String) # Added location
    image_path = Column(String, unique=True)
    device_id = Column(String, index=True)

# Pydantic Models (for API validation)
class DetectionBase(PydanticBaseModel):
    species: str
    confidence: float
    timestamp: datetime
    device_id: str
    location: str

class DetectionCreate(DetectionBase):
    pass

class DetectionOut(DetectionBase):
    id: int
    image_path: str

    class Config:
        from_attributes = True
        