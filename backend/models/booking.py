import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Date, Float, Text, Integer, ForeignKey, JSON, Numeric
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_number = Column(String(50), unique=True, nullable=False, index=True)

    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    booking_type = Column(String(20), nullable=False)  # product, guide

    product_id = Column(String(36), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    guide_id = Column(String(36), ForeignKey("guides.id", ondelete="SET NULL"), nullable=True)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="SET NULL"), nullable=True)

    booking_date = Column(Date, nullable=False)
    num_participants = Column(Integer, default=1)
    options = Column(JSON, nullable=True)

    guest_name = Column(String(200), nullable=True)
    guest_email = Column(String(255), nullable=True)
    guest_phone = Column(String(50), nullable=True)
    guest_nationality = Column(String(100), nullable=True)

    total_amount_usd = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="USD")

    status = Column(String(20), default="pending")  # pending, confirmed, cancelled, completed

    stripe_payment_intent_id = Column(String(255), nullable=True)
    stripe_session_id = Column(String(255), nullable=True)

    paid_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
