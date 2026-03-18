import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer
from database import Base


class MapSetting(Base):
    __tablename__ = "map_settings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mapbox_api_key = Column(String(500), nullable=True)
    default_latitude = Column(Float, default=37.5665)  # Seoul default
    default_longitude = Column(Float, default=126.9780)
    default_zoom = Column(Integer, default=12)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
