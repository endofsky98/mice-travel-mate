import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Date, Float, Text, Integer, JSON
from database import Base


class Festival(Base):
    __tablename__ = "festivals"

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

    category = Column(String(50), nullable=True)  # festival, performance, market, exhibition
    image_url = Column(String(1000), nullable=True)
    images = Column(JSON, nullable=True)

    venue_name = Column(String(500), nullable=True)
    address = Column(String(1000), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    website_url = Column(String(1000), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
