import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Float, ForeignKey, JSON
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    target_type = Column(String(20), nullable=False)  # restaurant, course, product, guide
    target_id = Column(String(36), nullable=False, index=True)

    rating = Column(Integer, nullable=False)  # 1-5
    content = Column(Text, nullable=False)
    images = Column(JSON, nullable=True)  # Array of image URLs, max 5

    status = Column(String(20), default="pending")  # pending, approved, deleted
    is_reported = Column(Boolean, default=False)
    report_reason = Column(String(50), nullable=True)
    report_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
