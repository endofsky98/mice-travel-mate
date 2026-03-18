import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey
from database import Base


class Theme(Base):
    __tablename__ = "themes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name_en = Column(String(200), nullable=False)
    name_ko = Column(String(200), nullable=True)
    name_zh_cn = Column(String(200), nullable=True)
    name_zh_tw = Column(String(200), nullable=True)
    name_ja = Column(String(200), nullable=True)
    name_es = Column(String(200), nullable=True)
    name_th = Column(String(200), nullable=True)
    name_vi = Column(String(200), nullable=True)
    name_fr = Column(String(200), nullable=True)

    description_en = Column(Text, nullable=True)
    description_ko = Column(Text, nullable=True)

    icon = Column(String(100), nullable=True)
    color = Column(String(20), nullable=True)  # hex color for map layer
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ThemeSpot(Base):
    __tablename__ = "theme_spots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    theme_id = Column(String(36), ForeignKey("themes.id", ondelete="CASCADE"), nullable=False, index=True)
    target_type = Column(String(20), nullable=False)  # restaurant, course_spot, festival
    target_id = Column(String(36), nullable=False)
    display_order = Column(Integer, default=0)
