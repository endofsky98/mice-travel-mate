import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.sqlite import JSON
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    name = Column(String(100), nullable=False)
    nationality = Column(String(100), nullable=True)
    preferred_language = Column(String(10), default="en")
    provider = Column(String(20), default="local")  # local, google, apple
    provider_id = Column(String(255), nullable=True)
    role = Column(String(20), default="user")  # user, admin, superadmin
    is_active = Column(Boolean, default=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_type = Column(String(20), nullable=False)  # restaurant, course, product, guide
    target_id = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
