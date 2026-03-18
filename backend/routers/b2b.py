from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from database import get_db
from models.b2b import B2BPartner
from models.event import Event
from models.booking import Booking
from models.user import User
from auth.dependencies import get_current_user
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/b2b", tags=["B2B Partners"])


async def get_partner_for_user(user: User, db: AsyncSession) -> B2BPartner:
    """Get the B2B partner record associated with the current user."""
    result = await db.execute(
        select(B2BPartner).where(
            B2BPartner.user_id == user.id,
            B2BPartner.is_active == True,
        )
    )
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=403, detail="B2B partner access required")
    return partner


@router.get("/dashboard")
async def partner_dashboard(
    lang: str = Query("en"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get B2B partner dashboard stats."""
    partner = await get_partner_for_user(current_user, db)

    # Get assigned event IDs
    assigned_event_ids = partner.assigned_events or []

    # Count events
    events_count = 0
    if assigned_event_ids:
        events_result = await db.execute(
            select(func.count(Event.id)).where(Event.id.in_(assigned_event_ids))
        )
        events_count = events_result.scalar() or 0

    # Count bookings related to assigned events
    total_bookings = 0
    pending_bookings = 0
    confirmed_bookings = 0
    total_revenue = 0.0

    if assigned_event_ids:
        # Total bookings
        bookings_result = await db.execute(
            select(func.count(Booking.id)).where(
                Booking.event_id.in_(assigned_event_ids)
            )
        )
        total_bookings = bookings_result.scalar() or 0

        # Pending
        pending_result = await db.execute(
            select(func.count(Booking.id)).where(
                Booking.event_id.in_(assigned_event_ids),
                Booking.status == "pending",
            )
        )
        pending_bookings = pending_result.scalar() or 0

        # Confirmed
        confirmed_result = await db.execute(
            select(func.count(Booking.id)).where(
                Booking.event_id.in_(assigned_event_ids),
                Booking.status == "confirmed",
            )
        )
        confirmed_bookings = confirmed_result.scalar() or 0

        # Revenue
        revenue_result = await db.execute(
            select(func.sum(Booking.total_amount_usd)).where(
                Booking.event_id.in_(assigned_event_ids),
                Booking.status.in_(["confirmed", "completed"]),
            )
        )
        total_revenue = float(revenue_result.scalar() or 0)

    return {
        "partner": {
            "id": partner.id,
            "company_name": partner.company_name,
            "contact_name": partner.contact_name,
            "contact_email": partner.contact_email,
        },
        "stats": {
            "events_count": events_count,
            "bookings": {
                "total": total_bookings,
                "pending": pending_bookings,
                "confirmed": confirmed_bookings,
            },
            "total_revenue_usd": round(total_revenue, 2),
        },
        "landing_config": partner.landing_config,
    }


@router.get("/events")
async def partner_events(
    lang: str = Query("en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List the partner's assigned events."""
    partner = await get_partner_for_user(current_user, db)

    assigned_event_ids = partner.assigned_events or []
    if not assigned_event_ids:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
        }

    query = select(Event).where(Event.id.in_(assigned_event_ids))

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(Event.start_date.desc().nullslast()).offset(offset).limit(per_page)
    result = await db.execute(query)
    events = result.scalars().all()

    items = []
    for e in events:
        # Get booking count per event
        booking_count_result = await db.execute(
            select(func.count(Booking.id)).where(Booking.event_id == e.id)
        )
        booking_count = booking_count_result.scalar() or 0

        items.append({
            "id": e.id,
            "slug": e.slug,
            "name": get_multilingual_field(e, "name", lang),
            "description": get_multilingual_field(e, "description", lang),
            "venue_name": e.venue_name,
            "start_date": str(e.start_date) if e.start_date else None,
            "end_date": str(e.end_date) if e.end_date else None,
            "banner_image_url": e.banner_image_url,
            "is_active": e.is_active,
            "booking_count": booking_count,
        })

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
    }
