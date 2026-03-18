import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.booking import Booking
from models.product import Product
from models.guide import Guide
from schemas.booking import BookingCreate, BookingCancel
from auth.dependencies import get_current_user, get_current_user_optional
from models.user import User
from utils.helpers import generate_booking_number, serialize_booking
from utils.email import send_booking_confirmation_email, send_booking_cancellation_email
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/bookings", tags=["Bookings"])


@router.post("/")
async def create_booking(
    data: BookingCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    # Validate booking type
    if data.booking_type == "product" and not data.product_id:
        raise HTTPException(status_code=400, detail="product_id is required for product bookings")
    if data.booking_type == "guide" and not data.guide_id:
        raise HTTPException(status_code=400, detail="guide_id is required for guide bookings")

    # Verify product/guide exists
    if data.product_id:
        prod_result = await db.execute(select(Product).where(Product.id == data.product_id))
        product = prod_result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

    if data.guide_id:
        guide_result = await db.execute(select(Guide).where(Guide.id == data.guide_id))
        guide = guide_result.scalar_one_or_none()
        if not guide:
            raise HTTPException(status_code=404, detail="Guide not found")

    # Generate unique booking number
    booking_number = generate_booking_number()
    # Ensure uniqueness
    while True:
        existing = await db.execute(select(Booking).where(Booking.booking_number == booking_number))
        if not existing.scalar_one_or_none():
            break
        booking_number = generate_booking_number()

    booking = Booking(
        booking_number=booking_number,
        user_id=current_user.id if current_user else None,
        booking_type=data.booking_type,
        product_id=data.product_id,
        guide_id=data.guide_id,
        event_id=data.event_id,
        booking_date=data.booking_date,
        num_participants=data.num_participants,
        options=data.options,
        guest_name=data.guest_name or (current_user.name if current_user else None),
        guest_email=data.guest_email or (current_user.email if current_user else None),
        guest_phone=data.guest_phone,
        guest_nationality=data.guest_nationality or (current_user.nationality if current_user else None),
        total_amount_usd=data.total_amount_usd,
        currency=data.currency or "USD",
        status="pending",
    )
    db.add(booking)
    await db.flush()
    await db.refresh(booking)

    return serialize_booking(booking)


@router.post("/{booking_id}/checkout")
async def create_checkout_session(
    booking_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status != "pending":
        raise HTTPException(status_code=400, detail="Booking is not in pending status")

    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe is not configured")

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get item name
        item_name = f"Booking {booking.booking_number}"
        if booking.product_id:
            prod_result = await db.execute(select(Product).where(Product.id == booking.product_id))
            product = prod_result.scalar_one_or_none()
            if product:
                item_name = product.name_en
        elif booking.guide_id:
            guide_result = await db.execute(select(Guide).where(Guide.id == booking.guide_id))
            guide = guide_result.scalar_one_or_none()
            if guide:
                item_name = f"Guide: {guide.name_en}"

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": booking.currency.lower(),
                        "product_data": {
                            "name": item_name,
                            "description": f"Booking #{booking.booking_number}",
                        },
                        "unit_amount": int(float(booking.total_amount_usd) * 100),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
            metadata={
                "booking_id": booking.id,
                "booking_number": booking.booking_number,
            },
        )

        booking.stripe_session_id = session.id
        await db.flush()

        return {
            "checkout_url": session.url,
            "session_id": session.id,
        }
    except Exception as e:
        logger.error("Stripe error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Stripe is not configured")

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            booking_id = session.get("metadata", {}).get("booking_id")

            if booking_id:
                result = await db.execute(select(Booking).where(Booking.id == booking_id))
                booking = result.scalar_one_or_none()
                if booking:
                    booking.status = "confirmed"
                    booking.stripe_payment_intent_id = session.get("payment_intent")
                    booking.paid_at = datetime.utcnow()
                    await db.flush()

                    # Send confirmation email
                    email = booking.guest_email
                    if email:
                        item_name = ""
                        if booking.product_id:
                            prod_result = await db.execute(select(Product).where(Product.id == booking.product_id))
                            product = prod_result.scalar_one_or_none()
                            if product:
                                item_name = product.name_en
                        elif booking.guide_id:
                            guide_result = await db.execute(select(Guide).where(Guide.id == booking.guide_id))
                            guide = guide_result.scalar_one_or_none()
                            if guide:
                                item_name = guide.name_en

                        await send_booking_confirmation_email(
                            to_email=email,
                            booking_number=booking.booking_number,
                            booking_type=booking.booking_type,
                            booking_date=str(booking.booking_date),
                            total_amount=float(booking.total_amount_usd),
                            guest_name=booking.guest_name or "Guest",
                            item_name=item_name,
                        )

        return {"status": "ok"}
    except Exception as e:
        logger.error("Stripe webhook error: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my")
async def list_my_bookings(
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Booking).where(Booking.user_id == current_user.id)

    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    query = query.order_by(Booking.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    bookings = result.scalars().all()

    return {
        "items": [serialize_booking(b) for b in bookings],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/guest/{booking_number}")
async def guest_booking_lookup(
    booking_number: str,
    email: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Booking).where(
            Booking.booking_number == booking_number,
            Booking.guest_email == email,
        )
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return serialize_booking(booking)


@router.get("/{booking_id}")
async def get_booking(
    booking_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Only allow viewing if user owns the booking or is admin
    if current_user:
        if booking.user_id != current_user.id and current_user.role not in ("admin", "superadmin"):
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

    return serialize_booking(booking)


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: str,
    data: BookingCancel,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Authorization check
    if current_user:
        if booking.user_id != current_user.id and current_user.role not in ("admin", "superadmin"):
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

    if booking.status in ("cancelled", "completed"):
        raise HTTPException(status_code=400, detail=f"Booking is already {booking.status}")

    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_reason = data.cancellation_reason
    await db.flush()

    # Send cancellation email
    if booking.guest_email:
        await send_booking_cancellation_email(
            to_email=booking.guest_email,
            booking_number=booking.booking_number,
            guest_name=booking.guest_name or "Guest",
            reason=data.cancellation_reason or "",
        )

    return serialize_booking(booking)
