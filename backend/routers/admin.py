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
from models.coupon import Coupon, CouponUsage
from models.festival import Festival
from models.theme import Theme, ThemeSpot
from models.living_guide import LivingGuideCategory, LivingGuideArticle
from models.chat import ChatRoom, ChatMessage
from models.b2b import B2BPartner

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
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Booking)
    count_query = select(func.count(Booking.id))

    if status:
        query = query.where(Booking.status == status)
        count_query = count_query.where(Booking.status == status)

    if search:
        search_filter = (
            Booking.booking_number.ilike(f"%{search}%") |
            Booking.guest_name.ilike(f"%{search}%") |
            Booking.guest_email.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
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
    target_type: Optional[str] = Query(None),
    rating: Optional[int] = Query(None, ge=1, le=5),
    is_reported: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List reviews for admin dashboard, with filters."""
    query = select(Review)
    count_query = select(func.count(Review.id))

    if status:
        query = query.where(Review.status == status)
        count_query = count_query.where(Review.status == status)
    if target_type:
        query = query.where(Review.target_type == target_type)
        count_query = count_query.where(Review.target_type == target_type)
    if rating:
        query = query.where(Review.rating == rating)
        count_query = count_query.where(Review.rating == rating)
    if is_reported == "true":
        query = query.where(Review.is_reported == True)
        count_query = count_query.where(Review.is_reported == True)
    elif is_reported == "false":
        query = query.where(Review.is_reported == False)
        count_query = count_query.where(Review.is_reported == False)
    if search:
        query = query.where(Review.content.ilike(f"%{search}%"))
        count_query = count_query.where(Review.content.ilike(f"%{search}%"))

    count_result = await db.execute(count_query)
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
        "transition_type": b.transition_type or "slide",
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
        transition_type=data.get("transition_type", "slide"),
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
    if "transition_type" in data:
        banner.transition_type = data["transition_type"]

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
                "is_admin": u.role in ("admin", "superadmin"),
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


# ─────────────────────── Map Settings (Admin) ───────────────────────

@router.get("/settings/map")
async def admin_get_map_settings(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get map settings."""
    from models.map_setting import MapSetting

    result = await db.execute(select(MapSetting).limit(1))
    setting = result.scalar_one_or_none()

    if not setting:
        return {
            "mapbox_api_key": "",
            "default_center_lat": 37.5665,
            "default_center_lng": 126.978,
            "default_zoom": 12,
        }

    return {
        "mapbox_api_key": setting.mapbox_api_key or "",
        "default_center_lat": setting.default_latitude or 37.5665,
        "default_center_lng": setting.default_longitude or 126.978,
        "default_zoom": setting.default_zoom or 12,
    }


@router.put("/settings/map")
async def admin_update_map_settings(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update map settings."""
    from models.map_setting import MapSetting

    result = await db.execute(select(MapSetting).limit(1))
    setting = result.scalar_one_or_none()

    if not setting:
        setting = MapSetting(id=str(uuid.uuid4()))
        db.add(setting)

    if "mapbox_api_key" in data:
        setting.mapbox_api_key = data["mapbox_api_key"]
    if "default_center_lat" in data:
        setting.default_latitude = data["default_center_lat"]
    if "default_center_lng" in data:
        setting.default_longitude = data["default_center_lng"]
    if "default_zoom" in data:
        setting.default_zoom = data["default_zoom"]

    setting.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(setting)

    return {
        "mapbox_api_key": setting.mapbox_api_key or "",
        "default_center_lat": setting.default_latitude or 37.5665,
        "default_center_lng": setting.default_longitude or 126.978,
        "default_zoom": setting.default_zoom or 12,
    }


# ─────────────────────── Helper: multilingual serializer ───────────────────────

def serialize_ml(obj, prefix):
    """Serialize multilingual fields for a given prefix (e.g. 'name', 'description')."""
    result = {}
    for lang in SUPPORTED_LANG_CODES:
        result[lang] = getattr(obj, f"{prefix}_{lang}", None) or ""
    return result


def set_ml_fields(obj, data, prefix):
    """Set multilingual fields from a dict like {"en": "...", "ko": "..."}."""
    value = data.get(prefix)
    if isinstance(value, dict):
        for lang in SUPPORTED_LANG_CODES:
            if lang in value:
                setattr(obj, f"{prefix}_{lang}", value[lang])


# ─────────────────────── Coupons (Admin) ───────────────────────

def serialize_coupon(c):
    return {
        "id": c.id,
        "code": c.code,
        "name": c.name,
        "description": c.description,
        "discount_type": c.discount_type,
        "discount_value": float(c.discount_value) if c.discount_value else 0,
        "max_discount_usd": float(c.max_discount_usd) if c.max_discount_usd else None,
        "min_order_usd": float(c.min_order_usd) if c.min_order_usd else None,
        "applicable_to": c.applicable_to,
        "applicable_ids": c.applicable_ids,
        "applicable_categories": c.applicable_categories,
        "event_id": c.event_id,
        "start_date": c.start_date.isoformat() if c.start_date else None,
        "end_date": c.end_date.isoformat() if c.end_date else None,
        "total_limit": c.total_limit,
        "per_user_limit": c.per_user_limit,
        "used_count": c.used_count,
        "is_active": c.is_active,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }


@router.get("/coupons")
async def admin_list_coupons(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all coupons with pagination."""
    query = select(Coupon)
    count_query = select(func.count(Coupon.id))

    if search:
        search_filter = (
            Coupon.code.ilike(f"%{search}%") |
            Coupon.name.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(Coupon.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    coupons = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [serialize_coupon(c) for c in coupons],
        "total": total,
        "pages": pages,
    }


@router.post("/coupons")
async def admin_create_coupon(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new coupon."""
    coupon = Coupon(
        id=str(uuid.uuid4()),
        code=data.get("code", ""),
        name=data.get("name", ""),
        description=data.get("description"),
        discount_type=data.get("discount_type", "fixed"),
        discount_value=data.get("discount_value", 0),
        max_discount_usd=data.get("max_discount_usd"),
        min_order_usd=data.get("min_order_usd"),
        applicable_to=data.get("applicable_to", "all"),
        applicable_ids=data.get("applicable_ids"),
        applicable_categories=data.get("applicable_categories"),
        event_id=data.get("event_id") or None,
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        total_limit=data.get("total_limit"),
        per_user_limit=data.get("per_user_limit", 1),
        is_active=data.get("is_active", True),
    )
    db.add(coupon)
    await db.flush()
    await db.refresh(coupon)
    return serialize_coupon(coupon)


@router.put("/coupons/{coupon_id}")
async def admin_update_coupon(
    coupon_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a coupon."""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    for field in [
        "code", "name", "description", "discount_type", "discount_value",
        "max_discount_usd", "min_order_usd", "applicable_to", "applicable_ids",
        "applicable_categories", "event_id", "start_date", "end_date",
        "total_limit", "per_user_limit", "is_active",
    ]:
        if field in data:
            setattr(coupon, field, data[field])

    coupon.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(coupon)
    return serialize_coupon(coupon)


@router.patch("/coupons/{coupon_id}")
async def admin_patch_coupon(
    coupon_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Partially update a coupon (e.g., toggle is_active)."""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    if "is_active" in data:
        coupon.is_active = data["is_active"]

    coupon.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(coupon)
    return serialize_coupon(coupon)


@router.delete("/coupons/{coupon_id}")
async def admin_delete_coupon(
    coupon_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a coupon."""
    result = await db.execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")

    await db.delete(coupon)
    await db.flush()
    return {"message": "Coupon deleted"}


# ─────────────────────── Festivals (Admin) ───────────────────────

def serialize_festival(f):
    return {
        "id": f.id,
        "name": serialize_ml(f, "name"),
        "description": serialize_ml(f, "description"),
        "category": f.category,
        "image_url": f.image_url,
        "images": f.images,
        "venue_name": f.venue_name,
        "address": f.address,
        "latitude": f.latitude,
        "longitude": f.longitude,
        "start_date": f.start_date.isoformat() if f.start_date else None,
        "end_date": f.end_date.isoformat() if f.end_date else None,
        "website_url": f.website_url,
        "is_active": f.is_active,
        "created_at": f.created_at.isoformat() if f.created_at else None,
        "updated_at": f.updated_at.isoformat() if f.updated_at else None,
    }


@router.get("/festivals")
async def admin_list_festivals(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all festivals with pagination."""
    query = select(Festival)
    count_query = select(func.count(Festival.id))

    if search:
        search_filter = (
            Festival.name_en.ilike(f"%{search}%") |
            Festival.name_ko.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    if category:
        query = query.where(Festival.category == category)
        count_query = count_query.where(Festival.category == category)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(Festival.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    festivals = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [serialize_festival(f) for f in festivals],
        "total": total,
        "pages": pages,
    }


@router.post("/festivals")
async def admin_create_festival(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new festival."""
    festival = Festival(
        id=str(uuid.uuid4()),
        category=data.get("category"),
        image_url=data.get("image_url"),
        images=data.get("images"),
        venue_name=data.get("venue_name"),
        address=data.get("address"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        website_url=data.get("website_url"),
        is_active=data.get("is_active", True),
    )
    set_ml_fields(festival, data, "name")
    set_ml_fields(festival, data, "description")

    if not festival.name_en:
        festival.name_en = data.get("name", {}).get("en", "") if isinstance(data.get("name"), dict) else data.get("name_en", "")

    db.add(festival)
    await db.flush()
    await db.refresh(festival)
    return serialize_festival(festival)


@router.put("/festivals/{festival_id}")
async def admin_update_festival(
    festival_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a festival."""
    result = await db.execute(select(Festival).where(Festival.id == festival_id))
    festival = result.scalar_one_or_none()
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")

    for field in [
        "category", "image_url", "images", "venue_name", "address",
        "latitude", "longitude", "start_date", "end_date",
        "website_url", "is_active",
    ]:
        if field in data:
            setattr(festival, field, data[field])

    set_ml_fields(festival, data, "name")
    set_ml_fields(festival, data, "description")

    festival.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(festival)
    return serialize_festival(festival)


@router.delete("/festivals/{festival_id}")
async def admin_delete_festival(
    festival_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a festival."""
    result = await db.execute(select(Festival).where(Festival.id == festival_id))
    festival = result.scalar_one_or_none()
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")

    await db.delete(festival)
    await db.flush()
    return {"message": "Festival deleted"}


# ─────────────────────── Themes (Admin) ───────────────────────

def serialize_theme(t):
    return {
        "id": t.id,
        "name": serialize_ml(t, "name"),
        "description": serialize_ml(t, "description"),
        "icon": t.icon,
        "color": t.color,
        "display_order": t.display_order,
        "is_active": t.is_active,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
    }


def serialize_theme_spot(s):
    return {
        "id": s.id,
        "theme_id": s.theme_id,
        "target_type": s.target_type,
        "target_id": s.target_id,
        "display_order": s.display_order,
    }


@router.get("/themes")
async def admin_list_themes(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all themes with pagination."""
    query = select(Theme)
    count_query = select(func.count(Theme.id))

    if search:
        search_filter = (
            Theme.name_en.ilike(f"%{search}%") |
            Theme.name_ko.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(Theme.display_order, Theme.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    themes = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [serialize_theme(t) for t in themes],
        "total": total,
        "pages": pages,
    }


@router.post("/themes")
async def admin_create_theme(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new theme."""
    theme = Theme(
        id=str(uuid.uuid4()),
        icon=data.get("icon"),
        color=data.get("color"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
    )
    set_ml_fields(theme, data, "name")
    set_ml_fields(theme, data, "description")

    if not theme.name_en:
        theme.name_en = data.get("name", {}).get("en", "") if isinstance(data.get("name"), dict) else data.get("name_en", "")

    db.add(theme)
    await db.flush()
    await db.refresh(theme)
    return serialize_theme(theme)


@router.put("/themes/{theme_id}")
async def admin_update_theme(
    theme_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a theme."""
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    for field in ["icon", "color", "display_order", "is_active"]:
        if field in data:
            setattr(theme, field, data[field])

    set_ml_fields(theme, data, "name")
    set_ml_fields(theme, data, "description")

    theme.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(theme)
    return serialize_theme(theme)


@router.delete("/themes/{theme_id}")
async def admin_delete_theme(
    theme_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a theme and its spots."""
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    # Delete associated spots
    spots_result = await db.execute(select(ThemeSpot).where(ThemeSpot.theme_id == theme_id))
    spots = spots_result.scalars().all()
    for spot in spots:
        await db.delete(spot)

    await db.delete(theme)
    await db.flush()
    return {"message": "Theme deleted"}


@router.post("/themes/{theme_id}/spots")
async def admin_add_theme_spot(
    theme_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Add a spot to a theme."""
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Theme not found")

    spot = ThemeSpot(
        id=str(uuid.uuid4()),
        theme_id=theme_id,
        target_type=data.get("target_type", ""),
        target_id=data.get("target_id", ""),
        display_order=data.get("display_order", 0),
    )
    db.add(spot)
    await db.flush()
    await db.refresh(spot)
    return {
        "id": spot.id,
        "theme_id": spot.theme_id,
        "target_type": spot.target_type,
        "target_id": spot.target_id,
        "display_order": spot.display_order,
    }


@router.delete("/themes/{theme_id}/spots/{spot_id}")
async def admin_remove_theme_spot(
    theme_id: str,
    spot_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Remove a spot from a theme."""
    result = await db.execute(
        select(ThemeSpot).where(ThemeSpot.id == spot_id, ThemeSpot.theme_id == theme_id)
    )
    spot = result.scalar_one_or_none()
    if not spot:
        raise HTTPException(status_code=404, detail="Theme spot not found")

    await db.delete(spot)
    await db.flush()
    return {"message": "Theme spot removed"}


# ─────────────────────── Living Guide (Admin) ───────────────────────

def serialize_living_guide_category(c):
    return {
        "id": c.id,
        "name": serialize_ml(c, "name"),
        "icon": c.icon,
        "display_order": c.display_order,
        "is_active": c.is_active,
    }


def serialize_living_guide_article(a):
    return {
        "id": a.id,
        "category_id": a.category_id,
        "title": serialize_ml(a, "title"),
        "content": serialize_ml(a, "content"),
        "image_url": a.image_url,
        "display_order": a.display_order,
        "is_active": a.is_active,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
    }


@router.get("/living-guide/categories")
async def admin_list_living_guide_categories(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all living guide categories."""
    result = await db.execute(
        select(LivingGuideCategory).order_by(LivingGuideCategory.display_order)
    )
    categories = result.scalars().all()
    return {"items": [serialize_living_guide_category(c) for c in categories]}


@router.post("/living-guide/categories")
async def admin_create_living_guide_category(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a living guide category."""
    category = LivingGuideCategory(
        id=str(uuid.uuid4()),
        icon=data.get("icon"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
    )
    set_ml_fields(category, data, "name")

    if not category.name_en:
        category.name_en = data.get("name", {}).get("en", "") if isinstance(data.get("name"), dict) else data.get("name_en", "")

    db.add(category)
    await db.flush()
    await db.refresh(category)
    return serialize_living_guide_category(category)


@router.put("/living-guide/categories/{category_id}")
async def admin_update_living_guide_category(
    category_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a living guide category."""
    result = await db.execute(
        select(LivingGuideCategory).where(LivingGuideCategory.id == category_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for field in ["icon", "display_order", "is_active"]:
        if field in data:
            setattr(category, field, data[field])

    set_ml_fields(category, data, "name")

    await db.flush()
    await db.refresh(category)
    return serialize_living_guide_category(category)


@router.delete("/living-guide/categories/{category_id}")
async def admin_delete_living_guide_category(
    category_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a living guide category."""
    result = await db.execute(
        select(LivingGuideCategory).where(LivingGuideCategory.id == category_id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Delete associated articles
    articles_result = await db.execute(
        select(LivingGuideArticle).where(LivingGuideArticle.category_id == category_id)
    )
    articles = articles_result.scalars().all()
    for article in articles:
        await db.delete(article)

    await db.delete(category)
    await db.flush()
    return {"message": "Category deleted"}


@router.get("/living-guide/articles")
async def admin_list_living_guide_articles(
    category_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List living guide articles with pagination."""
    query = select(LivingGuideArticle)
    count_query = select(func.count(LivingGuideArticle.id))

    if category_id:
        query = query.where(LivingGuideArticle.category_id == category_id)
        count_query = count_query.where(LivingGuideArticle.category_id == category_id)

    if search:
        search_filter = (
            LivingGuideArticle.title_en.ilike(f"%{search}%") |
            LivingGuideArticle.title_ko.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(LivingGuideArticle.display_order, LivingGuideArticle.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    articles = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [serialize_living_guide_article(a) for a in articles],
        "total": total,
        "pages": pages,
    }


@router.post("/living-guide/articles")
async def admin_create_living_guide_article(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a living guide article."""
    article = LivingGuideArticle(
        id=str(uuid.uuid4()),
        category_id=data.get("category_id", ""),
        image_url=data.get("image_url"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
    )
    set_ml_fields(article, data, "title")
    set_ml_fields(article, data, "content")

    if not article.title_en:
        article.title_en = data.get("title", {}).get("en", "") if isinstance(data.get("title"), dict) else data.get("title_en", "")

    db.add(article)
    await db.flush()
    await db.refresh(article)
    return serialize_living_guide_article(article)


@router.put("/living-guide/articles/{article_id}")
async def admin_update_living_guide_article(
    article_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a living guide article."""
    result = await db.execute(
        select(LivingGuideArticle).where(LivingGuideArticle.id == article_id)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    for field in ["category_id", "image_url", "display_order", "is_active"]:
        if field in data:
            setattr(article, field, data[field])

    set_ml_fields(article, data, "title")
    set_ml_fields(article, data, "content")

    article.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(article)
    return serialize_living_guide_article(article)


@router.delete("/living-guide/articles/{article_id}")
async def admin_delete_living_guide_article(
    article_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a living guide article."""
    result = await db.execute(
        select(LivingGuideArticle).where(LivingGuideArticle.id == article_id)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    await db.delete(article)
    await db.flush()
    return {"message": "Article deleted"}


@router.get("/living-guide/categories/{category_id}/articles")
async def admin_list_articles_by_category(
    category_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List articles for a specific category."""
    result = await db.execute(
        select(LivingGuideArticle).where(
            LivingGuideArticle.category_id == category_id
        ).order_by(LivingGuideArticle.display_order)
    )
    articles = result.scalars().all()
    return {"items": [serialize_living_guide_article(a) for a in articles]}


@router.post("/living-guide/categories/{category_id}/articles")
async def admin_create_article_in_category(
    category_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create an article in a specific category."""
    data["category_id"] = category_id
    article = LivingGuideArticle(
        id=str(uuid.uuid4()),
        category_id=category_id,
        image_url=data.get("image_url"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
    )
    set_ml_fields(article, data, "title")
    set_ml_fields(article, data, "content")
    if not article.title_en:
        article.title_en = data.get("title", {}).get("en", "") if isinstance(data.get("title"), dict) else data.get("title_en", "")
    db.add(article)
    await db.flush()
    await db.refresh(article)
    return serialize_living_guide_article(article)


# ─────────────────────── Chat Monitoring (Admin) ───────────────────────

def serialize_chat_room(r):
    return {
        "id": r.id,
        "user_id": r.user_id,
        "guide_id": r.guide_id,
        "last_message": r.last_message,
        "last_message_at": r.last_message_at.isoformat() if r.last_message_at else None,
        "is_active": r.is_active,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


def serialize_chat_message(m):
    return {
        "id": m.id,
        "room_id": m.room_id,
        "sender_type": m.sender_type,
        "sender_id": m.sender_id,
        "message_type": m.message_type,
        "content": m.content,
        "image_url": m.image_url,
        "is_read": m.is_read,
        "is_reported": m.is_reported,
        "report_reason": m.report_reason,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }


@router.get("/chat/reported")
async def admin_list_reported_chats(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List reported chat messages."""
    query = select(ChatMessage).where(ChatMessage.is_reported == True)
    count_query = select(func.count(ChatMessage.id)).where(ChatMessage.is_reported == True)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(ChatMessage.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    messages = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [serialize_chat_message(m) for m in messages],
        "total": total,
        "pages": pages,
    }


@router.get("/chat/rooms/{room_id}/messages")
async def admin_get_chat_messages(
    room_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get messages for a specific chat room."""
    room_result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    query = select(ChatMessage).where(ChatMessage.room_id == room_id)
    count_query = select(func.count(ChatMessage.id)).where(ChatMessage.room_id == room_id)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(ChatMessage.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    messages = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "room": serialize_chat_room(room),
        "messages": [serialize_chat_message(m) for m in messages],
        "total": total,
        "pages": pages,
    }


@router.patch("/chat/messages/{message_id}/review")
async def admin_review_chat_message(
    message_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Review a reported chat message - dismiss report or take action."""
    result = await db.execute(select(ChatMessage).where(ChatMessage.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    action = data.get("action", "dismiss")  # dismiss, warn, delete

    if action == "dismiss":
        message.is_reported = False
        message.report_reason = None
    elif action == "delete":
        message.content = "[Message removed by admin]"
        message.is_reported = False
        message.report_reason = None
    elif action == "warn":
        message.is_reported = False
        message.report_reason = None

    await db.flush()
    await db.refresh(message)
    return serialize_chat_message(message)


@router.patch("/chat/rooms/{room_id}/sanction")
async def admin_sanction_chat_room(
    room_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Sanction a chat room - disable or enable."""
    result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    if "is_active" in data:
        room.is_active = data["is_active"]

    room.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(room)
    return serialize_chat_room(room)


# ─────────────────────── B2B Partners (Admin) ───────────────────────

def serialize_b2b_partner(p):
    return {
        "id": p.id,
        "user_id": p.user_id,
        "company_name": p.company_name,
        "contact_name": p.contact_name,
        "contact_email": p.contact_email,
        "contact_phone": p.contact_phone,
        "assigned_events": p.assigned_events,
        "landing_config": p.landing_config,
        "is_active": p.is_active,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }


@router.get("/b2b-partners")
async def admin_list_b2b_partners(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all B2B partners with pagination."""
    query = select(B2BPartner)
    count_query = select(func.count(B2BPartner.id))

    if search:
        search_filter = (
            B2BPartner.company_name.ilike(f"%{search}%") |
            B2BPartner.contact_name.ilike(f"%{search}%") |
            B2BPartner.contact_email.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    offset = (page - 1) * per_page
    query = query.order_by(B2BPartner.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    partners = result.scalars().all()

    pages = (total + per_page - 1) // per_page if per_page else 1

    return {
        "items": [serialize_b2b_partner(p) for p in partners],
        "total": total,
        "pages": pages,
    }


@router.post("/b2b-partners")
async def admin_create_b2b_partner(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new B2B partner."""
    partner = B2BPartner(
        id=str(uuid.uuid4()),
        user_id=data.get("user_id", ""),
        company_name=data.get("company_name", ""),
        contact_name=data.get("contact_name"),
        contact_email=data.get("contact_email"),
        contact_phone=data.get("contact_phone"),
        assigned_events=data.get("assigned_events"),
        landing_config=data.get("landing_config"),
        is_active=data.get("is_active", True),
    )
    db.add(partner)
    await db.flush()
    await db.refresh(partner)
    return serialize_b2b_partner(partner)


@router.put("/b2b-partners/{partner_id}")
async def admin_update_b2b_partner(
    partner_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a B2B partner."""
    result = await db.execute(select(B2BPartner).where(B2BPartner.id == partner_id))
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=404, detail="B2B Partner not found")

    for field in [
        "company_name", "contact_name", "contact_email", "contact_phone",
        "assigned_events", "landing_config", "is_active",
    ]:
        if field in data:
            setattr(partner, field, data[field])

    partner.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(partner)
    return serialize_b2b_partner(partner)


@router.delete("/b2b-partners/{partner_id}")
async def admin_delete_b2b_partner(
    partner_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a B2B partner."""
    result = await db.execute(select(B2BPartner).where(B2BPartner.id == partner_id))
    partner = result.scalar_one_or_none()
    if not partner:
        raise HTTPException(status_code=404, detail="B2B Partner not found")

    await db.delete(partner)
    await db.flush()
    return {"message": "B2B Partner deleted"}


# ─────────────────────── Route Aliases (Frontend compatibility) ───────────────────────

# Chat aliases - frontend uses /chat/reports instead of /chat/reported
@router.get("/chat/reports")
async def admin_list_reported_chats_alias(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await admin_list_reported_chats(page=page, per_page=per_page, admin=admin, db=db)


@router.patch("/chat/reports/{message_id}")
async def admin_review_chat_report_alias(
    message_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Handle report action (frontend format: {status: 'dismissed'|'warned'|'deleted'})."""
    status = data.get("status", "")
    action_map = {"dismissed": "dismiss", "warned": "warn", "deleted": "delete"}
    action = action_map.get(status, data.get("action", "dismiss"))
    return await admin_review_chat_message(message_id=message_id, data={"action": action}, admin=admin, db=db)


@router.delete("/chat/messages/{message_id}")
async def admin_delete_chat_message(
    message_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a chat message."""
    result = await db.execute(select(ChatMessage).where(ChatMessage.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    await db.delete(message)
    await db.flush()
    return {"message": "Message deleted"}


# B2B aliases - frontend uses /b2b/partners instead of /b2b-partners
@router.get("/b2b/partners")
async def admin_list_b2b_alias(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await admin_list_b2b_partners(search=search, page=page, per_page=per_page, admin=admin, db=db)


@router.post("/b2b/partners")
async def admin_create_b2b_alias(
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await admin_create_b2b_partner(data=data, admin=admin, db=db)


@router.put("/b2b/partners/{partner_id}")
async def admin_update_b2b_alias(
    partner_id: str,
    data: dict = Body(...),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await admin_update_b2b_partner(partner_id=partner_id, data=data, admin=admin, db=db)


@router.delete("/b2b/partners/{partner_id}")
async def admin_delete_b2b_alias(
    partner_id: str,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    return await admin_delete_b2b_partner(partner_id=partner_id, admin=admin, db=db)
