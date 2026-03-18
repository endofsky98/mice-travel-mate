import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Date, ForeignKey
from database import Base


class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(String(500), nullable=False, index=True)
    language = Column(String(10), nullable=True)
    result_count = Column(Integer, default=0)
    user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(100), nullable=True, index=True)
    user_id = Column(String(36), nullable=True)
    page_path = Column(String(500), nullable=True)
    referrer = Column(String(1000), nullable=True)
    event_slug = Column(String(255), nullable=True)
    language = Column(String(10), nullable=True)
    nationality = Column(String(100), nullable=True)
    user_agent = Column(String(1000), nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentView(Base):
    __tablename__ = "content_views"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target_type = Column(String(20), nullable=False, index=True)  # restaurant, course, product, guide
    target_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=True)
    session_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
