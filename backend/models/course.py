import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, Integer, ForeignKey
from database import Base


class Course(Base):
    __tablename__ = "courses"

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

    duration_type = Column(String(20), nullable=True)  # half_day, full_day, overnight_2d, overnight_3d
    theme = Column(String(50), nullable=True)  # history, nature, shopping, food_tour, nightview, kpop, local
    region = Column(String(50), nullable=True)  # seoul, busan, jeju, incheon, gyeongju
    difficulty = Column(String(20), nullable=True)  # easy, moderate, hard

    total_duration_minutes = Column(Integer, nullable=True)
    total_distance_km = Column(Float, nullable=True)
    estimated_transport_cost = Column(Float, nullable=True)

    image_url = Column(String(1000), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CourseSpot(Base):
    __tablename__ = "course_spots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    spot_order = Column(Integer, nullable=False, default=0)

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

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    stay_duration_minutes = Column(Integer, nullable=True)
    image_url = Column(String(1000), nullable=True)
    restaurant_id = Column(String(36), ForeignKey("restaurants.id", ondelete="SET NULL"), nullable=True)


class CourseSpotTransition(Base):
    __tablename__ = "course_spot_transitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    from_spot_id = Column(String(36), ForeignKey("course_spots.id", ondelete="CASCADE"), nullable=False)
    to_spot_id = Column(String(36), ForeignKey("course_spots.id", ondelete="CASCADE"), nullable=False)
    transport_mode = Column(String(20), nullable=True)  # walk, subway, bus, taxi
    duration_minutes = Column(Integer, nullable=True)
    distance_km = Column(Float, nullable=True)
    route_polyline = Column(Text, nullable=True)
