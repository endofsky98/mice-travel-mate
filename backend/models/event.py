import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Date, Float, Text, Integer, ForeignKey
from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(255), unique=True, nullable=False, index=True)

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

    venue_name = Column(String(500), nullable=True)
    venue_address = Column(String(1000), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    banner_image_url = Column(String(1000), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EventRestaurant(Base):
    __tablename__ = "event_restaurants"

    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id", ondelete="CASCADE"), primary_key=True)
    display_order = Column(Integer, default=0)


class EventCourse(Base):
    __tablename__ = "event_courses"

    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    display_order = Column(Integer, default=0)


class EventProduct(Base):
    __tablename__ = "event_products"

    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    display_order = Column(Integer, default=0)


class EventGuide(Base):
    __tablename__ = "event_guides"

    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    guide_id = Column(String(36), ForeignKey("guides.id", ondelete="CASCADE"), primary_key=True)
    display_order = Column(Integer, default=0)
