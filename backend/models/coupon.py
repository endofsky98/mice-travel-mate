import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey, JSON, Numeric, Date
from database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)

    discount_type = Column(String(20), nullable=False)  # fixed, percentage, upgrade
    discount_value = Column(Numeric(10, 2), nullable=False)  # amount or percentage
    max_discount_usd = Column(Numeric(10, 2), nullable=True)  # max discount for percentage

    min_order_usd = Column(Numeric(10, 2), nullable=True)
    applicable_to = Column(String(20), default="all")  # all, product, category
    applicable_ids = Column(JSON, nullable=True)  # specific product/category IDs
    applicable_categories = Column(JSON, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    total_limit = Column(Integer, nullable=True)  # total usage limit
    per_user_limit = Column(Integer, default=1)
    used_count = Column(Integer, default=0)

    # Event-specific coupon
    event_id = Column(String(36), ForeignKey("events.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CouponUsage(Base):
    __tablename__ = "coupon_usages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    coupon_id = Column(String(36), ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    booking_id = Column(String(36), ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    discount_amount_usd = Column(Numeric(10, 2), nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)
