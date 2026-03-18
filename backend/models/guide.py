import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, Date, ForeignKey, JSON, Numeric
from database import Base


class Guide(Base):
    __tablename__ = "guides"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name_en = Column(String(500), nullable=False)
    name_ko = Column(String(500), nullable=True)
    name_zh_cn = Column(String(500), nullable=True)
    name_zh_tw = Column(String(500), nullable=True)
    name_ja = Column(String(500), nullable=True)
    name_es = Column(String(500), nullable=True)

    bio_en = Column(Text, nullable=True)
    bio_ko = Column(Text, nullable=True)
    bio_zh_cn = Column(Text, nullable=True)
    bio_zh_tw = Column(Text, nullable=True)
    bio_ja = Column(Text, nullable=True)
    bio_es = Column(Text, nullable=True)

    profile_image_url = Column(String(1000), nullable=True)
    languages = Column(JSON, nullable=True)  # [{language: "English", proficiency: "native"}, ...]
    specialties = Column(JSON, nullable=True)  # ["history", "food", "shopping", "kpop"]
    regions = Column(JSON, nullable=True)  # ["seoul", "busan"]

    price_per_hour_usd = Column(Numeric(10, 2), nullable=True)
    price_half_day_usd = Column(Numeric(10, 2), nullable=True)
    price_full_day_usd = Column(Numeric(10, 2), nullable=True)

    services_en = Column(Text, nullable=True)
    services_ko = Column(Text, nullable=True)
    services_zh_cn = Column(Text, nullable=True)
    services_zh_tw = Column(Text, nullable=True)
    services_ja = Column(Text, nullable=True)
    services_es = Column(Text, nullable=True)

    status = Column(String(20), default="active")  # active, resting, inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GuideAvailability(Base):
    __tablename__ = "guide_availability"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    guide_id = Column(String(36), ForeignKey("guides.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    is_available = Column(Boolean, default=True)
