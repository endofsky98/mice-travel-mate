import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, JSON
from database import Base


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    guide_id = Column(String(36), ForeignKey("guides.id", ondelete="CASCADE"), nullable=False, index=True)

    last_message = Column(Text, nullable=True)
    last_message_at = Column(DateTime, nullable=True)
    user_unread_count = Column(Integer, default=0)
    guide_unread_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_type = Column(String(10), nullable=False)  # user, guide
    sender_id = Column(String(36), nullable=False)

    message_type = Column(String(20), default="text")  # text, image
    content = Column(Text, nullable=True)
    image_url = Column(String(1000), nullable=True)

    is_read = Column(Boolean, default=False)
    is_reported = Column(Boolean, default=False)
    report_reason = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
