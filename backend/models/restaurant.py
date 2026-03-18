import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, JSON
from database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name_en = Column(String(500), nullable=False)
    name_ko = Column(String(500), nullable=True)
    name_zh_cn = Column(String(500), nullable=True)
    name_zh_tw = Column(String(500), nullable=True)
    name_ja = Column(String(500), nullable=True)
    name_es = Column(String(500), nullable=True)
    name_th = Column(String(500), nullable=True)
    name_vi = Column(String(500), nullable=True)
    name_fr = Column(String(500), nullable=True)

    description_en = Column(Text, nullable=True)
    description_ko = Column(Text, nullable=True)
    description_zh_cn = Column(Text, nullable=True)
    description_zh_tw = Column(Text, nullable=True)
    description_ja = Column(Text, nullable=True)
    description_es = Column(Text, nullable=True)
    description_th = Column(Text, nullable=True)
    description_vi = Column(Text, nullable=True)
    description_fr = Column(Text, nullable=True)

    category = Column(String(50), nullable=True)
    price_range = Column(Integer, nullable=True)

    address = Column(String(1000), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    phone = Column(String(50), nullable=True)

    opening_hours = Column(JSON, nullable=True)
    menu_highlights = Column(JSON, nullable=True)
    images = Column(JSON, nullable=True)

    avg_rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
