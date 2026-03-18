import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, Date, ForeignKey, JSON, Numeric
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name_en = Column(String(500), nullable=False)
    name_ko = Column(String(500), nullable=True)
    name_zh_cn = Column(String(500), nullable=True)
    name_zh_tw = Column(String(500), nullable=True)
    name_ja = Column(String(500), nullable=True)
    name_es = Column(String(500), nullable=True)

    description_en = Column(Text, nullable=True)
    description_ko = Column(Text, nullable=True)
    description_zh_cn = Column(Text, nullable=True)
    description_zh_tw = Column(Text, nullable=True)
    description_ja = Column(Text, nullable=True)
    description_es = Column(Text, nullable=True)

    category = Column(String(50), nullable=True)  # tour, experience, show, activity
    price_usd = Column(Numeric(10, 2), nullable=True)
    duration_hours = Column(Float, nullable=True)
    region = Column(String(50), nullable=True)

    min_participants = Column(Integer, nullable=True)
    max_participants = Column(Integer, nullable=True)

    includes_en = Column(JSON, nullable=True)
    includes_ko = Column(JSON, nullable=True)
    includes_zh_cn = Column(JSON, nullable=True)
    includes_zh_tw = Column(JSON, nullable=True)
    includes_ja = Column(JSON, nullable=True)
    includes_es = Column(JSON, nullable=True)

    excludes_en = Column(JSON, nullable=True)
    excludes_ko = Column(JSON, nullable=True)
    excludes_zh_cn = Column(JSON, nullable=True)
    excludes_zh_tw = Column(JSON, nullable=True)
    excludes_ja = Column(JSON, nullable=True)
    excludes_es = Column(JSON, nullable=True)

    itinerary = Column(JSON, nullable=True)

    meeting_point = Column(String(500), nullable=True)
    meeting_point_lat = Column(Float, nullable=True)
    meeting_point_lng = Column(Float, nullable=True)
    dismissal_point = Column(String(500), nullable=True)

    cancellation_policy_en = Column(Text, nullable=True)
    cancellation_policy_ko = Column(Text, nullable=True)
    cancellation_policy_zh_cn = Column(Text, nullable=True)
    cancellation_policy_zh_tw = Column(Text, nullable=True)
    cancellation_policy_ja = Column(Text, nullable=True)
    cancellation_policy_es = Column(Text, nullable=True)

    images = Column(JSON, nullable=True)
    status = Column(String(20), default="active")  # active, hidden, soldout

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductInventory(Base):
    __tablename__ = "product_inventory"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    total_slots = Column(Integer, default=0)
    booked_slots = Column(Integer, default=0)
