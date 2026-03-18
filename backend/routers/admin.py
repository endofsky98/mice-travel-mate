import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from typing import Optional, List
from pydantic import BaseModel

from config import settings
from database import get_db
from auth.dependencies import get_current_admin
from models.user import User, Bookmark
from models.event import Event, EventRestaurant, EventCourse, EventProduct, EventGuide
from models.restaurant import Restaurant
from models.course import Course, CourseSpot, CourseSpotTransition
from models.transport import TransportRoute, TransportTip
from models.product import Product, ProductInventory
from models.guide import Guide, GuideAvailability
from models.booking import Booking
from models.language import Language, UITranslation
from models.review import Review
from models.analytics import SearchLog, VisitorLog
from models.banner import RollingBanner

from schemas.event import EventCreate, EventUpdate, EventLinkIds
from schemas.restaurant import RestaurantCreate, RestaurantUpdate
from schemas.course import CourseCreate, CourseUpdate, CourseSpotCreate, CourseSpotTransitionCreate
from schemas.transport import TransportRouteCreate, TransportRouteUpdate, TransportTipCreate, TransportTipUpdate
from schemas.product import ProductCreate, ProductUpdate
from schemas.guide import GuideCreate, GuideUpdate, GuideAvailabilityUpdate
from schemas.booking import BookingStatusUpdate
from schemas.language import LanguageCreate, LanguageUpdate, UITranslationCreate, UITranslationUpdate, UITranslationBulkCreate

from utils.helpers import (
    serialize_event, serialize_restaurant, serialize_course, serialize_product,
    serialize_guide, serialize_booking, serialize_transport_route, serialize_transport_tip,
    serialize_course_spot, serialize_course_spot_transition,
    get_multilingual_field,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])

SUPPORTED_LANG_CODES = ["en", "ko", "zh_cn", "zh_tw", "ja", "es", "th", "vi", "fr"]


# ─────────────────────── Dashboard ───────────────────────

@router.get("/dashboard")
async def dashboard(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    events_count = len((await db.execute(select(Event))).scalars().all())
    restaurants_count = len((await db.execute(select(Restaurant))).scalars().all())
    courses_count = len((await db.execute(select(Course))).scalars().all())
    products_count = len((await db.execute(select(Product))).scalars().all())
    guides_count = len((await db.execute(select(Guide))).scalars().all())
    bookings_count = len((await db.execute(select(Booking))).scalars().all())
    users_count = len((await db.execute(select(User))).scalars().all())

    pending_bookings = len((await db.execute(
        select(Booking).where(Booking.status == "pending")
    )).scalars().all())

    confirmed_bookings = len((await db.execute(
        select(Booking).where(Booking.status == "confirmed")
    )).scalars().all())

    return {
        "events": events_count,
        "restaurants": restaurants_count,
        "courses": courses_count,
        "products": products_count,
        "guides": guides_count,
        "bookings": {
            "total": bookings_count,
            "pending": pending_bookings,
            "confirmed": confirmed_bookings,
        },
        "users": users_count,
    }


@router.get("/dashboard/stats")
async def dashboard_stats(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Dashboard stats in the format expected by the frontend."""
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Today's bookings count
    today_bookings_result = await db.execute(
        select(func.count(Booking.id)).where(
            func.date(Booking.created_at) == today
        )
    )
    today_bookings = today_bookings_result.scalar() or 0

    # Today's booking amount
    today_amount_result = await db.execute(
        select(func.coalesce(func.sum(Booking.total_amount_usd), 0)).where(
            func.date(Booking.created_at) == today
        )
    )
    today_booking_amount = float(today_amount_result.scalar() or 0)

    # Total content counts
    total_restaurants = (await db.execute(select(func.count(Restaurant.id)))).scalar() or 0
    total_courses = (await db.execute(select(func.count(Course.id)))).scalar() or 0
    total_products = (await db.execute(select(func.count(Product.id)))).scalar() or 0
    total_guides = (await db.execute(select(func.count(Guide.id)))).scalar() or 0

    # Today's visitors (unique sessions)
    today_visitors_result = await db.execute(
        select(func.count(func.distinct(VisitorLog.session_id))).where(
            func.date(VisitorLog.created_at) == today
        )
    )
    today_visitors = today_visitors_result.scalar() or 0

    # Yesterday's visitors for trend calculation
    yesterday_visitors_result = await db.execute(
        select(func.count(func.distinct(VisitorLog.session_id))).where(
            func.date(VisitorLog.created_at) == yesterday
        )
    )
    yesterday_visitors = yesterday_visitors_result.scalar() or 0

    # Visitor trend (percentage change)
    if yesterday_visitors > 0:
        visitor_trend = round(((today_visitors - yesterday_visitors) / yesterday_visitors) * 100, 1)
    else:
        visitor_trend = 0

    # Untranslated count: count items that have English text but missing other languages
    # Simple heuristic: count UITranslation keys that exist for 'en' but not for all active languages
    active_langs_result = await db.execute(
        select(Language.code).where(Language.is_active == True)
    )
    active_langs = [row[0] for row in active_langs_result.all()]

    en_keys_result = await db.execute(
        select(func.count(func.distinct(UITranslation.key))).where(
            UITranslation.language_code == "en"
        )
    )
    en_key_count = en_keys_result.scalar() or 0

    untranslated_count = 0
    for lang_code in active_langs:
        if lang_code == "en":
            continue
        lang_keys_result = await db.execute(
            select(func.count(func.distinct(UITranslation.key))).where(
                UITranslation.language_code == lang_code
            )
        )
        lang_key_count = lang_keys_result.scalar() or 0
        if lang_key_count < en_key_count:
            untranslated_count += (en_key_count - lang_key_count)

    return {
        "today_bookings": today_bookings,
        "today_booking_amount": today_booking_amount,
        "total_restaurants": total_restaurants,
        "total_courses": total_courses,
        "total_products": total_products,
        "total_guides": total_guides,
        "today_visitors": today_visitors,
        "visitor_trend": visitor_trend,
        "untranslated_count": untranslated_count,
    }


# ─────────────────────── Events CRUD ───────────────────────

@router.get("/events")
async def admin_list_events(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Event)
    count_query = select(func.count(Event.id))

    if search:
        search_filter = Event.venue_name.ilike(f"%{search}%")
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    if offset is not None and limit is not None:
        query = query.order_by(Event.created_at.desc()).offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.order_by(Event.created_at.desc()).offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    events = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": [serialize_event(e) for e in events], "total": total, "pages": pages}


@router.post("/events")
async def admin_create_event(
    data: EventCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    # Check slug uniqueness
    existing = await db.execute(select(Event).where(Event.slug == data.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Event slug already exists")

    event = Event(**data.model_dump())
    db.add(event)
    await db.flush()
    await db.refresh(event)
    return serialize_event(event)


@router.get("/events/{event_id}")
async def admin_get_event(
    event_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return serialize_event(event)


@router.put("/events/{event_id}")
async def admin_update_event(
    event_id: str,
    data: EventUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    event.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(event)
    return serialize_event(event)


@router.delete("/events/{event_id}")
async def admin_delete_event(
    event_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    await db.delete(event)
    await db.flush()
    return {"message": "Event deleted"}


@router.post("/events/{event_id}/links")
async def admin_link_event_items(
    event_id: str,
    data: EventLinkIds,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if data.restaurant_ids is not None:
        # Remove existing links
        existing = await db.execute(select(EventRestaurant).where(EventRestaurant.event_id == event_id))
        for er in existing.scalars().all():
            await db.delete(er)
        # Add new links
        for i, rid in enumerate(data.restaurant_ids):
            db.add(EventRestaurant(event_id=event_id, restaurant_id=rid, display_order=i))

    if data.course_ids is not None:
        existing = await db.execute(select(EventCourse).where(EventCourse.event_id == event_id))
        for ec in existing.scalars().all():
            await db.delete(ec)
        for i, cid in enumerate(data.course_ids):
            db.add(EventCourse(event_id=event_id, course_id=cid, display_order=i))

    if data.product_ids is not None:
        existing = await db.execute(select(EventProduct).where(EventProduct.event_id == event_id))
        for ep in existing.scalars().all():
            await db.delete(ep)
        for i, pid in enumerate(data.product_ids):
            db.add(EventProduct(event_id=event_id, product_id=pid, display_order=i))

    if data.guide_ids is not None:
        existing = await db.execute(select(EventGuide).where(EventGuide.event_id == event_id))
        for eg in existing.scalars().all():
            await db.delete(eg)
        for i, gid in enumerate(data.guide_ids):
            db.add(EventGuide(event_id=event_id, guide_id=gid, display_order=i))

    await db.flush()
    return {"message": "Event links updated"}


# ─────────────────────── Restaurants CRUD ───────────────────────

@router.get("/restaurants")
async def admin_list_restaurants(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Restaurant)
    count_query = select(func.count(Restaurant.id))

    if search:
        search_filter = Restaurant.address.ilike(f"%{search}%")
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    if offset is not None and limit is not None:
        query = query.order_by(Restaurant.created_at.desc()).offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.order_by(Restaurant.created_at.desc()).offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    restaurants = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": [serialize_restaurant(r) for r in restaurants], "total": total, "pages": pages}


@router.post("/restaurants")
async def admin_create_restaurant(
    data: RestaurantCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    restaurant = Restaurant(**data.model_dump())
    db.add(restaurant)
    await db.flush()
    await db.refresh(restaurant)
    return serialize_restaurant(restaurant)


@router.get("/restaurants/{restaurant_id}")
async def admin_get_restaurant(
    restaurant_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return serialize_restaurant(restaurant)


@router.put("/restaurants/{restaurant_id}")
async def admin_update_restaurant(
    restaurant_id: str,
    data: RestaurantUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(restaurant, key, value)
    restaurant.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(restaurant)
    return serialize_restaurant(restaurant)


@router.delete("/restaurants/{restaurant_id}")
async def admin_delete_restaurant(
    restaurant_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    await db.delete(restaurant)
    await db.flush()
    return {"message": "Restaurant deleted"}


# ─────────────────────── Courses CRUD ───────────────────────

@router.get("/courses")
async def admin_list_courses(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    count_query = select(func.count(Course.id))

    if search:
        search_filter = Course.theme.ilike(f"%{search}%")
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    if offset is not None and limit is not None:
        query = query.order_by(Course.created_at.desc()).offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.order_by(Course.created_at.desc()).offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    courses = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": [serialize_course(c) for c in courses], "total": total, "pages": pages}


@router.post("/courses")
async def admin_create_course(
    data: CourseCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    course = Course(**data.model_dump())
    db.add(course)
    await db.flush()
    await db.refresh(course)
    return serialize_course(course)


@router.get("/courses/{course_id}")
async def admin_get_course(
    course_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    spots_result = await db.execute(
        select(CourseSpot).where(CourseSpot.course_id == course_id).order_by(CourseSpot.spot_order)
    )
    spots = spots_result.scalars().all()

    transitions_result = await db.execute(
        select(CourseSpotTransition).where(CourseSpotTransition.course_id == course_id)
    )
    transitions = transitions_result.scalars().all()

    course_data = serialize_course(course)
    course_data["spots"] = [serialize_course_spot(s) for s in spots]
    course_data["transitions"] = [serialize_course_spot_transition(t) for t in transitions]
    return course_data


@router.put("/courses/{course_id}")
async def admin_update_course(
    course_id: str,
    data: CourseUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    course.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(course)
    return serialize_course(course)


@router.delete("/courses/{course_id}")
async def admin_delete_course(
    course_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)
    await db.flush()
    return {"message": "Course deleted"}


@router.post("/courses/{course_id}/spots")
async def admin_add_course_spot(
    course_id: str,
    data: CourseSpotCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Course not found")

    spot = CourseSpot(course_id=course_id, **data.model_dump())
    db.add(spot)
    await db.flush()
    await db.refresh(spot)
    return serialize_course_spot(spot)


@router.put("/courses/{course_id}/spots/{spot_id}")
async def admin_update_course_spot(
    course_id: str,
    spot_id: str,
    data: CourseSpotCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(CourseSpot).where(CourseSpot.id == spot_id, CourseSpot.course_id == course_id))
    spot = result.scalar_one_or_none()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(spot, key, value)
    await db.flush()
    await db.refresh(spot)
    return serialize_course_spot(spot)


@router.delete("/courses/{course_id}/spots/{spot_id}")
async def admin_delete_course_spot(
    course_id: str,
    spot_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(CourseSpot).where(CourseSpot.id == spot_id, CourseSpot.course_id == course_id))
    spot = result.scalar_one_or_none()
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")

    await db.delete(spot)
    await db.flush()
    return {"message": "Spot deleted"}


@router.post("/courses/{course_id}/transitions")
async def admin_add_course_transition(
    course_id: str,
    data: CourseSpotTransitionCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Course not found")

    transition = CourseSpotTransition(course_id=course_id, **data.model_dump())
    db.add(transition)
    await db.flush()
    await db.refresh(transition)
    return serialize_course_spot_transition(transition)


@router.delete("/courses/{course_id}/transitions/{transition_id}")
async def admin_delete_course_transition(
    course_id: str,
    transition_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CourseSpotTransition).where(
            CourseSpotTransition.id == transition_id,
            CourseSpotTransition.course_id == course_id,
        )
    )
    transition = result.scalar_one_or_none()
    if not transition:
        raise HTTPException(status_code=404, detail="Transition not found")

    await db.delete(transition)
    await db.flush()
    return {"message": "Transition deleted"}


# ─────────────────────── Products CRUD ───────────────────────

@router.get("/products")
async def admin_list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Product)
    count_query = select(func.count(Product.id))

    if search:
        search_filter = Product.category.ilike(f"%{search}%")
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    if offset is not None and limit is not None:
        query = query.order_by(Product.created_at.desc()).offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.order_by(Product.created_at.desc()).offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    products = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": [serialize_product(p) for p in products], "total": total, "pages": pages}


@router.post("/products")
async def admin_create_product(
    data: ProductCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    product = Product(**data.model_dump())
    db.add(product)
    await db.flush()
    await db.refresh(product)
    return serialize_product(product)


@router.get("/products/{product_id}")
async def admin_get_product(
    product_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(product)


@router.put("/products/{product_id}")
async def admin_update_product(
    product_id: str,
    data: ProductUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    product.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(product)
    return serialize_product(product)


@router.delete("/products/{product_id}")
async def admin_delete_product(
    product_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.flush()
    return {"message": "Product deleted"}


@router.post("/products/{product_id}/inventory")
async def admin_set_product_inventory(
    product_id: str,
    date: str = Query(...),
    total_slots: int = Query(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    from datetime import date as date_type
    result = await db.execute(select(Product).where(Product.id == product_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Product not found")

    d = date_type.fromisoformat(date)
    inv_result = await db.execute(
        select(ProductInventory).where(
            ProductInventory.product_id == product_id,
            ProductInventory.date == d,
        )
    )
    inv = inv_result.scalar_one_or_none()
    if inv:
        inv.total_slots = total_slots
    else:
        inv = ProductInventory(product_id=product_id, date=d, total_slots=total_slots, booked_slots=0)
        db.add(inv)

    await db.flush()
    if inv:
        await db.refresh(inv)
    return {
        "id": inv.id,
        "product_id": inv.product_id,
        "date": str(inv.date),
        "total_slots": inv.total_slots,
        "booked_slots": inv.booked_slots,
    }


# ─────────────────────── Guides CRUD ───────────────────────

@router.get("/guides")
async def admin_list_guides(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Guide)
    count_query = select(func.count(Guide.id))

    if search:
        search_filter = Guide.status.ilike(f"%{search}%")
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    if offset is not None and limit is not None:
        query = query.order_by(Guide.created_at.desc()).offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.order_by(Guide.created_at.desc()).offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    guides = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": [serialize_guide(g) for g in guides], "total": total, "pages": pages}


@router.post("/guides")
async def admin_create_guide(
    data: GuideCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    guide = Guide(**data.model_dump())
    db.add(guide)
    await db.flush()
    await db.refresh(guide)
    return serialize_guide(guide)


@router.get("/guides/{guide_id}")
async def admin_get_guide(
    guide_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Guide).where(Guide.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")
    return serialize_guide(guide)


@router.put("/guides/{guide_id}")
async def admin_update_guide(
    guide_id: str,
    data: GuideUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Guide).where(Guide.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(guide, key, value)
    guide.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(guide)
    return serialize_guide(guide)


@router.delete("/guides/{guide_id}")
async def admin_delete_guide(
    guide_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Guide).where(Guide.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    await db.delete(guide)
    await db.flush()
    return {"message": "Guide deleted"}


@router.post("/guides/{guide_id}/availability")
async def admin_set_guide_availability(
    guide_id: str,
    data: GuideAvailabilityUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Guide).where(Guide.id == guide_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Guide not found")

    avail_result = await db.execute(
        select(GuideAvailability).where(
            GuideAvailability.guide_id == guide_id,
            GuideAvailability.date == data.date,
        )
    )
    avail = avail_result.scalar_one_or_none()
    if avail:
        avail.is_available = data.is_available
    else:
        avail = GuideAvailability(guide_id=guide_id, date=data.date, is_available=data.is_available)
        db.add(avail)

    await db.flush()
    if avail:
        await db.refresh(avail)
    return {
        "id": avail.id,
        "guide_id": avail.guide_id,
        "date": str(avail.date),
        "is_available": avail.is_available,
    }


# ─────────────────────── Transport Routes CRUD ───────────────────────

@router.get("/transport/routes")
async def admin_list_transport_routes(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(select(TransportRoute))
    total = len(count_result.scalars().all())

    result = await db.execute(
        select(TransportRoute).offset(offset).limit(limit)
    )
    routes = result.scalars().all()
    return {"items": [serialize_transport_route(r) for r in routes], "total": total}


@router.post("/transport/routes")
async def admin_create_transport_route(
    data: TransportRouteCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    route = TransportRoute(**data.model_dump())
    db.add(route)
    await db.flush()
    await db.refresh(route)
    return serialize_transport_route(route)


@router.put("/transport/routes/{route_id}")
async def admin_update_transport_route(
    route_id: str,
    data: TransportRouteUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TransportRoute).where(TransportRoute.id == route_id))
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Transport route not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(route, key, value)
    route.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(route)
    return serialize_transport_route(route)


@router.delete("/transport/routes/{route_id}")
async def admin_delete_transport_route(
    route_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TransportRoute).where(TransportRoute.id == route_id))
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Transport route not found")

    await db.delete(route)
    await db.flush()
    return {"message": "Transport route deleted"}


# ─────────────────────── Transport Tips CRUD ───────────────────────

@router.get("/transport/tips")
async def admin_list_transport_tips(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TransportTip).order_by(TransportTip.display_order))
    tips = result.scalars().all()
    return {"items": [serialize_transport_tip(t) for t in tips]}


@router.post("/transport/tips")
async def admin_create_transport_tip(
    data: TransportTipCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    tip = TransportTip(**data.model_dump())
    db.add(tip)
    await db.flush()
    await db.refresh(tip)
    return serialize_transport_tip(tip)


@router.put("/transport/tips/{tip_id}")
async def admin_update_transport_tip(
    tip_id: str,
    data: TransportTipUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TransportTip).where(TransportTip.id == tip_id))
    tip = result.scalar_one_or_none()
    if not tip:
        raise HTTPException(status_code=404, detail="Transport tip not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tip, key, value)
    tip.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(tip)
    return serialize_transport_tip(tip)


@router.delete("/transport/tips/{tip_id}")
async def admin_delete_transport_tip(
    tip_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TransportTip).where(TransportTip.id == tip_id))
    tip = result.scalar_one_or_none()
    if not tip:
        raise HTTPException(status_code=404, detail="Transport tip not found")

    await db.delete(tip)
    await db.flush()
    return {"message": "Transport tip deleted"}


# ─────────────────────── Bookings (Admin) ───────────────────────

@router.get("/bookings")
async def admin_list_bookings(
    status: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Booking)
    if status:
        query = query.where(Booking.status == status)

    count_result = await db.execute(select(func.count(Booking.id)).where(
        Booking.status == status if status else True
    ))
    total = count_result.scalar() or 0

    # Sort order
    if sort == "oldest":
        query = query.order_by(Booking.created_at.asc())
    else:
        query = query.order_by(Booking.created_at.desc())

    # Support both offset/limit and page/per_page
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    bookings = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": [serialize_booking(b) for b in bookings], "total": total, "pages": pages}


@router.put("/bookings/{booking_id}/status")
async def admin_update_booking_status(
    booking_id: str,
    data: BookingStatusUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    valid_statuses = ["pending", "confirmed", "cancelled", "completed"]
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    booking.status = data.status
    if data.status == "cancelled":
        booking.cancelled_at = datetime.utcnow()
    elif data.status == "confirmed":
        booking.paid_at = booking.paid_at or datetime.utcnow()
    booking.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(booking)

    return serialize_booking(booking)


@router.post("/bookings/{booking_id}/refund")
async def admin_refund_booking(
    booking_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not booking.stripe_payment_intent_id:
        raise HTTPException(status_code=400, detail="No payment to refund")

    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe is not configured")

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        refund = stripe.Refund.create(
            payment_intent=booking.stripe_payment_intent_id,
        )

        booking.status = "cancelled"
        booking.cancelled_at = datetime.utcnow()
        booking.cancellation_reason = "Refunded by admin"
        booking.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(booking)

        return {
            "message": "Refund processed",
            "refund_id": refund.id,
            "booking": serialize_booking(booking),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refund error: {str(e)}")


@router.patch("/bookings/{booking_id}")
async def admin_patch_booking(
    booking_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Patch a booking (e.g. update status via PATCH)."""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if "status" in data:
        valid_statuses = ["pending", "confirmed", "cancelled", "completed"]
        if data["status"] not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        booking.status = data["status"]
        if data["status"] == "cancelled":
            booking.cancelled_at = datetime.utcnow()
        elif data["status"] == "confirmed":
            booking.paid_at = booking.paid_at or datetime.utcnow()

    booking.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(booking)
    return serialize_booking(booking)


# ─────────────────────── Reviews (Admin) ───────────────────────

@router.get("/reviews")
async def admin_list_reviews(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List reviews for admin dashboard, optionally filtered by status."""
    query = select(Review)
    if status:
        query = query.where(Review.status == status)

    count_result = await db.execute(
        select(func.count(Review.id)).where(
            Review.status == status if status else True
        )
    )
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(Review.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    reviews = result.scalars().all()

    # Fetch user names
    user_ids = list({r.user_id for r in reviews})
    users_map = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        for u in users_result.scalars().all():
            users_map[u.id] = u

    # Fetch target names (best effort)
    items = []
    for r in reviews:
        target_name = ""
        if r.target_type == "restaurant":
            t = (await db.execute(select(Restaurant).where(Restaurant.id == r.target_id))).scalar_one_or_none()
            if t:
                target_name = get_multilingual_field(t, "name", "en") or ""
        elif r.target_type == "product":
            t = (await db.execute(select(Product).where(Product.id == r.target_id))).scalar_one_or_none()
            if t:
                target_name = get_multilingual_field(t, "name", "en") or ""
        elif r.target_type == "course":
            t = (await db.execute(select(Course).where(Course.id == r.target_id))).scalar_one_or_none()
            if t:
                target_name = get_multilingual_field(t, "name", "en") or ""
        elif r.target_type == "guide":
            t = (await db.execute(select(Guide).where(Guide.id == r.target_id))).scalar_one_or_none()
            if t:
                target_name = get_multilingual_field(t, "name", "en") or ""

        items.append({
            "id": r.id,
            "user_id": r.user_id,
            "user_name": users_map.get(r.user_id, None) and users_map[r.user_id].name,
            "target_type": r.target_type,
            "target_id": r.target_id,
            "target_name": target_name,
            "rating": r.rating,
            "content": r.content,
            "images": r.images,
            "status": r.status,
            "is_reported": r.is_reported,
            "report_count": r.report_count,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {"items": items, "total": total, "pages": pages}


@router.patch("/reviews/{review_id}")
async def admin_patch_review(
    review_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Approve or delete a review."""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if "status" in data:
        valid_statuses = ["pending", "approved", "deleted"]
        if data["status"] not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        review.status = data["status"]

    review.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(review)

    return {
        "id": review.id,
        "status": review.status,
        "updated_at": review.updated_at.isoformat() if review.updated_at else None,
    }


# ─────────────────────── Analytics (Admin) ───────────────────────

@router.get("/analytics/searches")
async def admin_analytics_searches(
    per_page: int = Query(10, ge=1, le=100),
    period: int = Query(30, ge=1, le=365),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get popular search keywords for admin dashboard."""
    since = datetime.utcnow() - timedelta(days=period)

    top_queries_result = await db.execute(
        select(
            SearchLog.query,
            func.count(SearchLog.id).label("count"),
        )
        .where(SearchLog.created_at >= since)
        .group_by(SearchLog.query)
        .order_by(func.count(SearchLog.id).desc())
        .limit(per_page)
    )
    items = [
        {"keyword": row[0], "count": row[1]}
        for row in top_queries_result.all()
    ]

    return {"items": items}


@router.get("/analytics/visitors")
async def admin_analytics_visitors(
    period: int = Query(30, ge=1, le=365),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get visitor statistics for admin analytics page."""
    since = datetime.utcnow() - timedelta(days=period)

    total_result = await db.execute(
        select(func.count(VisitorLog.id)).where(VisitorLog.created_at >= since)
    )
    total_visits = total_result.scalar() or 0

    unique_result = await db.execute(
        select(func.count(func.distinct(VisitorLog.session_id))).where(VisitorLog.created_at >= since)
    )
    unique_sessions = unique_result.scalar() or 0

    # By language
    lang_result = await db.execute(
        select(VisitorLog.language, func.count(VisitorLog.id))
        .where(VisitorLog.created_at >= since)
        .group_by(VisitorLog.language)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(20)
    )
    by_language = [{"language": row[0] or "unknown", "count": row[1]} for row in lang_result.all()]

    # By nationality
    nat_result = await db.execute(
        select(VisitorLog.nationality, func.count(VisitorLog.id))
        .where(VisitorLog.created_at >= since)
        .group_by(VisitorLog.nationality)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(20)
    )
    by_nationality = [{"nationality": row[0] or "unknown", "count": row[1]} for row in nat_result.all()]

    # Top pages
    page_result = await db.execute(
        select(VisitorLog.page_path, func.count(VisitorLog.id))
        .where(VisitorLog.created_at >= since)
        .group_by(VisitorLog.page_path)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(20)
    )
    top_pages = [{"page": row[0] or "/", "count": row[1]} for row in page_result.all()]

    return {
        "period_days": period,
        "total_visits": total_visits,
        "unique_sessions": unique_sessions,
        "by_language": by_language,
        "by_nationality": by_nationality,
        "top_pages": top_pages,
    }


@router.get("/analytics/content")
async def admin_analytics_content(
    period: int = Query(30, ge=1, le=365),
    per_page: int = Query(10, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get content view statistics for admin analytics page."""
    from models.analytics import ContentView

    since = datetime.utcnow() - timedelta(days=period)

    top_items_result = await db.execute(
        select(
            ContentView.target_type,
            ContentView.target_id,
            func.count(ContentView.id).label("view_count"),
        )
        .where(ContentView.created_at >= since)
        .group_by(ContentView.target_type, ContentView.target_id)
        .order_by(func.count(ContentView.id).desc())
        .limit(per_page)
    )
    items = [
        {"target_type": row[0], "target_id": row[1], "view_count": row[2]}
        for row in top_items_result.all()
    ]

    return {"items": items}


@router.get("/analytics/bookings")
async def admin_analytics_bookings(
    period: int = Query(30, ge=1, le=365),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get booking statistics for admin analytics page."""
    since = datetime.utcnow() - timedelta(days=period)

    total_result = await db.execute(
        select(func.count(Booking.id)).where(Booking.created_at >= since)
    )
    total_bookings = total_result.scalar() or 0

    total_revenue_result = await db.execute(
        select(func.coalesce(func.sum(Booking.total_amount_usd), 0)).where(
            Booking.created_at >= since, Booking.status.in_(["confirmed", "completed"])
        )
    )
    total_revenue = float(total_revenue_result.scalar() or 0)

    pending_result = await db.execute(
        select(func.count(Booking.id)).where(
            Booking.created_at >= since, Booking.status == "pending"
        )
    )
    pending = pending_result.scalar() or 0

    confirmed_result = await db.execute(
        select(func.count(Booking.id)).where(
            Booking.created_at >= since, Booking.status == "confirmed"
        )
    )
    confirmed = confirmed_result.scalar() or 0

    cancelled_result = await db.execute(
        select(func.count(Booking.id)).where(
            Booking.created_at >= since, Booking.status == "cancelled"
        )
    )
    cancelled = cancelled_result.scalar() or 0

    return {
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "pending": pending,
        "confirmed": confirmed,
        "cancelled": cancelled,
    }


@router.get("/analytics/events")
async def admin_analytics_events(
    period: int = Query(30, ge=1, le=365),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get event comparison data for admin analytics page."""
    since = datetime.utcnow() - timedelta(days=period)

    # Get events with their booking counts
    events_result = await db.execute(select(Event))
    events = events_result.scalars().all()

    items = []
    for event in events:
        booking_count_result = await db.execute(
            select(func.count(Booking.id)).where(
                Booking.event_id == event.id,
                Booking.created_at >= since,
            )
        )
        booking_count = booking_count_result.scalar() or 0

        revenue_result = await db.execute(
            select(func.coalesce(func.sum(Booking.total_amount_usd), 0)).where(
                Booking.event_id == event.id,
                Booking.created_at >= since,
                Booking.status.in_(["confirmed", "completed"]),
            )
        )
        revenue = float(revenue_result.scalar() or 0)

        items.append({
            "id": event.id,
            "name": get_multilingual_field(event, "name", "en"),
            "bookings": booking_count,
            "revenue": revenue,
        })

    items.sort(key=lambda x: x["bookings"], reverse=True)
    return {"items": items}


# ─────────────────────── Banners (Admin) ───────────────────────

def serialize_banner_admin(b: RollingBanner) -> dict:
    """Serialize banner for admin (returns all language fields as dicts)."""
    title = {}
    subtitle = {}
    for lang in SUPPORTED_LANG_CODES:
        t = getattr(b, f"title_{lang}", None)
        if t:
            title[lang] = t
        s = getattr(b, f"subtitle_{lang}", None)
        if s:
            subtitle[lang] = s

    return {
        "id": b.id,
        "title": title,
        "subtitle": subtitle,
        "image_url": b.image_url,
        "link_url": b.link_url,
        "display_order": b.display_order,
        "is_active": b.is_active,
        "event_id": b.event_id,
        "rolling_interval": b.rolling_interval,
        "created_at": b.created_at.isoformat() if b.created_at else None,
        "updated_at": b.updated_at.isoformat() if b.updated_at else None,
    }


@router.get("/banners")
async def admin_list_banners(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all banners for admin management."""
    result = await db.execute(select(RollingBanner).order_by(RollingBanner.display_order))
    banners = result.scalars().all()
    return {"items": [serialize_banner_admin(b) for b in banners]}


@router.post("/banners")
async def admin_create_banner(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new banner."""
    banner = RollingBanner(
        id=str(uuid.uuid4()),
        image_url=data.get("image_url"),
        link_url=data.get("link_url"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
        event_id=data.get("event_id") or None,
        rolling_interval=data.get("rolling_interval", 4),
    )
    # Set multilingual title/subtitle fields
    title = data.get("title", {})
    subtitle = data.get("subtitle", {})
    if isinstance(title, dict):
        for lang in SUPPORTED_LANG_CODES:
            if lang in title:
                setattr(banner, f"title_{lang}", title[lang])
    if isinstance(subtitle, dict):
        for lang in SUPPORTED_LANG_CODES:
            if lang in subtitle:
                setattr(banner, f"subtitle_{lang}", subtitle[lang])

    # Ensure at least title_en is set
    if not banner.title_en:
        banner.title_en = title.get("en", "")

    db.add(banner)
    await db.flush()
    await db.refresh(banner)
    return serialize_banner_admin(banner)


@router.put("/banners/reorder")
async def admin_reorder_banners(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Reorder banners by updating display_order."""
    items = data.get("items", [])
    for item in items:
        result = await db.execute(select(RollingBanner).where(RollingBanner.id == item["id"]))
        banner = result.scalar_one_or_none()
        if banner:
            banner.display_order = item["display_order"]

    await db.flush()
    return {"message": "Banners reordered"}


@router.put("/banners/{banner_id}")
async def admin_update_banner(
    banner_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a banner."""
    result = await db.execute(select(RollingBanner).where(RollingBanner.id == banner_id))
    banner = result.scalar_one_or_none()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    if "image_url" in data:
        banner.image_url = data["image_url"]
    if "link_url" in data:
        banner.link_url = data["link_url"]
    if "display_order" in data:
        banner.display_order = data["display_order"]
    if "is_active" in data:
        banner.is_active = data["is_active"]
    if "event_id" in data:
        banner.event_id = data["event_id"] or None
    if "rolling_interval" in data:
        banner.rolling_interval = data["rolling_interval"]

    title = data.get("title")
    if isinstance(title, dict):
        for lang in SUPPORTED_LANG_CODES:
            if lang in title:
                setattr(banner, f"title_{lang}", title[lang])

    subtitle = data.get("subtitle")
    if isinstance(subtitle, dict):
        for lang in SUPPORTED_LANG_CODES:
            if lang in subtitle:
                setattr(banner, f"subtitle_{lang}", subtitle[lang])

    banner.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(banner)
    return serialize_banner_admin(banner)


@router.patch("/banners/{banner_id}")
async def admin_patch_banner(
    banner_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Partially update a banner (e.g., toggle is_active)."""
    result = await db.execute(select(RollingBanner).where(RollingBanner.id == banner_id))
    banner = result.scalar_one_or_none()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    if "is_active" in data:
        banner.is_active = data["is_active"]
    if "display_order" in data:
        banner.display_order = data["display_order"]

    banner.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(banner)
    return serialize_banner_admin(banner)


@router.delete("/banners/{banner_id}")
async def admin_delete_banner(
    banner_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a banner."""
    result = await db.execute(select(RollingBanner).where(RollingBanner.id == banner_id))
    banner = result.scalar_one_or_none()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    await db.delete(banner)
    await db.flush()
    return {"message": "Banner deleted"}


# ─────────────────────── Users (Admin) ───────────────────────

@router.get("/users")
async def admin_list_users(
    role: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(User)
    count_query = select(func.count(User.id))

    if role:
        query = query.where(User.role == role)
        count_query = count_query.where(User.role == role)

    if search:
        search_filter = (
            User.name.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # Support both offset/limit and page/per_page
    if offset is not None and limit is not None:
        query = query.order_by(User.created_at.desc()).offset(offset).limit(limit)
    else:
        actual_offset = (page - 1) * per_page
        query = query.order_by(User.created_at.desc()).offset(actual_offset).limit(per_page)

    result = await db.execute(query)
    users = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "nationality": u.nationality,
                "preferred_language": u.preferred_language,
                "provider": u.provider,
                "role": u.role,
                "is_active": u.is_active,
                "is_admin": u.role == "admin",
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None,
            }
            for u in users
        ],
        "total": total,
        "pages": pages,
    }


@router.put("/users/{user_id}")
async def admin_update_user(
    user_id: str,
    name: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    role: Optional[str] = Query(None),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if name is not None:
        user.name = name
    if is_active is not None:
        user.is_active = is_active
    if role is not None:
        user.role = role
    user.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "is_active": user.is_active,
        "is_admin": user.role == "admin",
    }


@router.patch("/users/{user_id}")
async def admin_patch_user(
    user_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Patch a user (e.g., toggle admin status)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "is_admin" in data:
        user.role = "admin" if data["is_admin"] else "user"
    if "name" in data:
        user.name = data["name"]
    if "is_active" in data:
        user.is_active = data["is_active"]
    if "role" in data:
        user.role = data["role"]

    user.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "is_active": user.is_active,
        "is_admin": user.role == "admin",
    }


@router.post("/users/{user_id}/make-admin")
async def admin_make_admin(
    user_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = "admin"
    user.updated_at = datetime.utcnow()
    await db.flush()

    return {"message": f"User {user.email} is now an admin"}


# ─────────────────────── Languages CRUD ───────────────────────

@router.get("/languages")
async def admin_list_languages(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Language).order_by(Language.display_order))
    languages = result.scalars().all()
    return {
        "items": [
            {
                "code": lang.code,
                "name": lang.name_en,
                "name_en": lang.name_en,
                "name_native": lang.name_native,
                "is_active": lang.is_active,
                "display_order": lang.display_order,
            }
            for lang in languages
        ]
    }


@router.post("/languages")
async def admin_create_language(
    data: LanguageCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(select(Language).where(Language.code == data.code))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Language code already exists")

    language = Language(**data.model_dump())
    db.add(language)
    await db.flush()
    await db.refresh(language)
    return {
        "code": language.code,
        "name_en": language.name_en,
        "name_native": language.name_native,
        "is_active": language.is_active,
        "display_order": language.display_order,
    }


@router.put("/languages/{code}")
async def admin_update_language(
    code: str,
    data: LanguageUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Language).where(Language.code == code))
    language = result.scalar_one_or_none()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(language, key, value)
    await db.flush()
    await db.refresh(language)
    return {
        "code": language.code,
        "name_en": language.name_en,
        "name_native": language.name_native,
        "is_active": language.is_active,
        "display_order": language.display_order,
    }


@router.patch("/languages/{code}")
async def admin_patch_language(
    code: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Patch a language (e.g., toggle is_active)."""
    result = await db.execute(select(Language).where(Language.code == code))
    language = result.scalar_one_or_none()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    if "is_active" in data:
        language.is_active = data["is_active"]
    if "name_en" in data:
        language.name_en = data["name_en"]
    if "name_native" in data:
        language.name_native = data["name_native"]
    if "display_order" in data:
        language.display_order = data["display_order"]

    await db.flush()
    await db.refresh(language)
    return {
        "code": language.code,
        "name": language.name_en,
        "name_en": language.name_en,
        "name_native": language.name_native,
        "is_active": language.is_active,
        "display_order": language.display_order,
    }


@router.delete("/languages/{code}")
async def admin_delete_language(
    code: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Language).where(Language.code == code))
    language = result.scalar_one_or_none()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    await db.delete(language)
    await db.flush()
    return {"message": "Language deleted"}


# ─────────────────────── UI Translations CRUD ───────────────────────

@router.get("/translations")
async def admin_list_translations(
    lang: Optional[str] = Query(None),
    language_code: Optional[str] = Query(None),
    limit: int = Query(500, ge=1, le=2000),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List translations. Supports both 'lang' and 'language_code' params.
    Returns items grouped by key with values dict for each language."""
    # Support both param names
    filter_lang = lang or language_code

    # Get all distinct keys
    all_keys_result = await db.execute(
        select(func.distinct(UITranslation.key)).order_by(UITranslation.key).offset(offset).limit(limit)
    )
    all_keys = [row[0] for row in all_keys_result.all()]

    # Get translations for these keys (all languages)
    if all_keys:
        translations_result = await db.execute(
            select(UITranslation).where(UITranslation.key.in_(all_keys))
        )
        translations = translations_result.scalars().all()
    else:
        translations = []

    # Group by key
    key_values = {}
    for t in translations:
        if t.key not in key_values:
            key_values[t.key] = {}
        key_values[t.key][t.language_code] = t.value

    items = [
        {"key": key, "values": key_values.get(key, {})}
        for key in all_keys
    ]

    total_keys_result = await db.execute(select(func.count(func.distinct(UITranslation.key))))
    total = total_keys_result.scalar() or 0

    return {"items": items, "total": total}


@router.post("/translations")
async def admin_create_translation(
    data: dict = Body(None),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a translation. Accepts either {key, value, lang} or UITranslationCreate format."""
    if data and "lang" in data:
        # Frontend format: {key, value, lang}
        key = data.get("key")
        value = data.get("value")
        language_code = data.get("lang")
    elif data and "language_code" in data:
        # Original schema format
        key = data.get("key")
        value = data.get("value")
        language_code = data.get("language_code")
    else:
        raise HTTPException(status_code=400, detail="Invalid translation data")

    if not key or not value or not language_code:
        raise HTTPException(status_code=400, detail="key, value, and lang are required")

    # Check if key already exists for this language
    existing = await db.execute(
        select(UITranslation).where(
            UITranslation.language_code == language_code,
            UITranslation.key == key,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Translation key already exists for this language")

    translation = UITranslation(language_code=language_code, key=key, value=value)
    db.add(translation)
    await db.flush()
    await db.refresh(translation)
    return {
        "id": translation.id,
        "language_code": translation.language_code,
        "key": translation.key,
        "value": translation.value,
    }


@router.post("/translations/bulk")
async def admin_bulk_create_translations(
    data: UITranslationBulkCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    created = 0
    updated = 0
    for key, value in data.translations.items():
        existing = await db.execute(
            select(UITranslation).where(
                UITranslation.language_code == data.language_code,
                UITranslation.key == key,
            )
        )
        trans = existing.scalar_one_or_none()
        if trans:
            trans.value = value
            updated += 1
        else:
            db.add(UITranslation(language_code=data.language_code, key=key, value=value))
            created += 1

    await db.flush()
    return {"created": created, "updated": updated}


@router.put("/translations/{translation_id}")
async def admin_update_translation_by_id(
    translation_id: str,
    data: UITranslationUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UITranslation).where(UITranslation.id == translation_id))
    translation = result.scalar_one_or_none()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")

    translation.value = data.value
    await db.flush()
    await db.refresh(translation)
    return {
        "id": translation.id,
        "language_code": translation.language_code,
        "key": translation.key,
        "value": translation.value,
    }


@router.put("/translations")
async def admin_update_translation_by_key(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a translation by key + lang (frontend format)."""
    key = data.get("key")
    value = data.get("value")
    language_code = data.get("lang") or data.get("language_code")

    if not key or value is None or not language_code:
        raise HTTPException(status_code=400, detail="key, value, and lang are required")

    result = await db.execute(
        select(UITranslation).where(
            UITranslation.language_code == language_code,
            UITranslation.key == key,
        )
    )
    translation = result.scalar_one_or_none()
    if not translation:
        # Create if not exists (upsert behavior)
        translation = UITranslation(language_code=language_code, key=key, value=value)
        db.add(translation)
        await db.flush()
        await db.refresh(translation)
    else:
        translation.value = value
        await db.flush()
        await db.refresh(translation)

    return {
        "id": translation.id,
        "language_code": translation.language_code,
        "key": translation.key,
        "value": translation.value,
    }


@router.delete("/translations/{translation_id}")
async def admin_delete_translation(
    translation_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UITranslation).where(UITranslation.id == translation_id))
    translation = result.scalar_one_or_none()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")

    await db.delete(translation)
    await db.flush()
    return {"message": "Translation deleted"}
