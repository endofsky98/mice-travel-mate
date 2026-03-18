import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, JSON
from database import Base


class TransportRoute(Base):
    __tablename__ = "transport_routes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    from_name_en = Column(String(500), nullable=False)
    from_name_ko = Column(String(500), nullable=True)
    from_name_zh_cn = Column(String(500), nullable=True)
    from_name_zh_tw = Column(String(500), nullable=True)
    from_name_ja = Column(String(500), nullable=True)
    from_name_es = Column(String(500), nullable=True)

    to_name_en = Column(String(500), nullable=False)
    to_name_ko = Column(String(500), nullable=True)
    to_name_zh_cn = Column(String(500), nullable=True)
    to_name_zh_tw = Column(String(500), nullable=True)
    to_name_ja = Column(String(500), nullable=True)
    to_name_es = Column(String(500), nullable=True)

    from_latitude = Column(Float, nullable=True)
    from_longitude = Column(Float, nullable=True)
    to_latitude = Column(Float, nullable=True)
    to_longitude = Column(Float, nullable=True)

    transport_modes = Column(JSON, nullable=True)  # Array of {mode, duration, cost, instructions}
    route_polyline = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TransportTip(Base):
    __tablename__ = "transport_tips"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    title_en = Column(String(500), nullable=False)
    title_ko = Column(String(500), nullable=True)
    title_zh_cn = Column(String(500), nullable=True)
    title_zh_tw = Column(String(500), nullable=True)
    title_ja = Column(String(500), nullable=True)
    title_es = Column(String(500), nullable=True)

    content_en = Column(Text, nullable=True)
    content_ko = Column(Text, nullable=True)
    content_zh_cn = Column(Text, nullable=True)
    content_zh_tw = Column(Text, nullable=True)
    content_ja = Column(Text, nullable=True)
    content_es = Column(Text, nullable=True)

    category = Column(String(20), nullable=True)  # tmoney, taxi, app, pass, general
    icon = Column(String(100), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
