import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Float, ForeignKey
from database import Base


class RollingBanner(Base):
    __tablename__ = "rolling_banners"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    title_en = Column(String(500), nullable=False)
    title_ko = Column(String(500), nullable=True)
    title_zh_cn = Column(String(500), nullable=True)
    title_zh_tw = Column(String(500), nullable=True)
    title_ja = Column(String(500), nullable=True)
    title_es = Column(String(500), nullable=True)
    title_th = Column(String(500), nullable=True)
    title_vi = Column(String(500), nullable=True)
    title_fr = Column(String(500), nullable=True)

    subtitle_en = Column(String(1000), nullable=True)
    subtitle_ko = Column(String(1000), nullable=True)
    subtitle_zh_cn = Column(String(1000), nullable=True)
    subtitle_zh_tw = Column(String(1000), nullable=True)
    subtitle_ja = Column(String(1000), nullable=True)
    subtitle_es = Column(String(1000), nullable=True)
    subtitle_th = Column(String(1000), nullable=True)
    subtitle_vi = Column(String(1000), nullable=True)
    subtitle_fr = Column(String(1000), nullable=True)

    image_url = Column(String(1000), nullable=True)
    link_url = Column(String(1000), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # Optional: show only for specific events
    event_id = Column(String(36), ForeignKey("events.id", ondelete="SET NULL"), nullable=True)

    # Rolling interval in seconds (3-5)
    rolling_interval = Column(Integer, default=4)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
