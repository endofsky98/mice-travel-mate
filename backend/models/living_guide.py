import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, JSON
from database import Base


class LivingGuideCategory(Base):
    __tablename__ = "living_guide_categories"

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

    icon = Column(String(100), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class LivingGuideArticle(Base):
    __tablename__ = "living_guide_articles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(String(36), nullable=False, index=True)

    title_en = Column(String(500), nullable=False)
    title_ko = Column(String(500), nullable=True)
    title_zh_cn = Column(String(500), nullable=True)
    title_zh_tw = Column(String(500), nullable=True)
    title_ja = Column(String(500), nullable=True)
    title_es = Column(String(500), nullable=True)
    title_th = Column(String(500), nullable=True)
    title_vi = Column(String(500), nullable=True)
    title_fr = Column(String(500), nullable=True)

    content_en = Column(Text, nullable=True)
    content_ko = Column(Text, nullable=True)
    content_zh_cn = Column(Text, nullable=True)
    content_zh_tw = Column(Text, nullable=True)
    content_ja = Column(Text, nullable=True)
    content_es = Column(Text, nullable=True)
    content_th = Column(Text, nullable=True)
    content_vi = Column(Text, nullable=True)
    content_fr = Column(Text, nullable=True)

    image_url = Column(String(1000), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
