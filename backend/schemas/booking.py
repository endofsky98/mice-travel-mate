from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import date


class BookingCreate(BaseModel):
    booking_type: str  # product, guide
    product_id: Optional[str] = None
    guide_id: Optional[str] = None
    event_id: Optional[str] = None
    booking_date: date
    num_participants: int = 1
    options: Optional[Any] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_nationality: Optional[str] = None
    total_amount_usd: float
    currency: Optional[str] = "USD"


class BookingCancel(BaseModel):
    cancellation_reason: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    status: str  # pending, confirmed, cancelled, completed


class GuestBookingLookup(BaseModel):
    booking_number: str
    email: str
