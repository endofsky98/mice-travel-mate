from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.event import Event, EventRestaurant, EventCourse, EventProduct, EventGuide
from models.restaurant import Restaurant
from models.course import Course
from models.product import Product
from models.guide import Guide
from utils.helpers import serialize_event, serialize_restaurant, serialize_course, serialize_product, serialize_guide

router = APIRouter(prefix="/api/v1/events", tags=["Events"])


@router.get("/")
async def list_events(
    lang: str = Query("en"),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Event)
    if is_active is not None:
        query = query.where(Event.is_active == is_active)
    query = query.order_by(Event.start_date.desc()).offset(offset).limit(limit)

    result = await db.execute(query)
    events = result.scalars().all()

    # Count total
    count_query = select(Event)
    if is_active is not None:
        count_query = count_query.where(Event.is_active == is_active)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    return {
        "items": [serialize_event(e, lang) for e in events],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{slug}")
async def get_event(
    slug: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.slug == slug))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return serialize_event(event, lang)


@router.get("/{slug}/landing")
async def get_event_landing(
    slug: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    # Get event
    result = await db.execute(select(Event).where(Event.slug == slug))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Get linked restaurants
    r_result = await db.execute(
        select(Restaurant)
        .join(EventRestaurant, EventRestaurant.restaurant_id == Restaurant.id)
        .where(EventRestaurant.event_id == event.id)
        .order_by(EventRestaurant.display_order)
    )
    restaurants = r_result.scalars().all()

    # Get linked courses
    c_result = await db.execute(
        select(Course)
        .join(EventCourse, EventCourse.course_id == Course.id)
        .where(EventCourse.event_id == event.id)
        .order_by(EventCourse.display_order)
    )
    courses = c_result.scalars().all()

    # Get linked products
    p_result = await db.execute(
        select(Product)
        .join(EventProduct, EventProduct.product_id == Product.id)
        .where(EventProduct.event_id == event.id)
        .order_by(EventProduct.display_order)
    )
    products = p_result.scalars().all()

    # Get linked guides
    g_result = await db.execute(
        select(Guide)
        .join(EventGuide, EventGuide.guide_id == Guide.id)
        .where(EventGuide.event_id == event.id)
        .order_by(EventGuide.display_order)
    )
    guides = g_result.scalars().all()

    return {
        "event": serialize_event(event, lang),
        "restaurants": [serialize_restaurant(r, lang) for r in restaurants],
        "courses": [serialize_course(c, lang) for c in courses],
        "products": [serialize_product(p, lang) for p in products],
        "guides": [serialize_guide(g, lang) for g in guides],
    }
