import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

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
)

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


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


# ─────────────────────── Events CRUD ───────────────────────

@router.get("/events")
async def admin_list_events(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(select(Event))
    total = len(count_result.scalars().all())

    result = await db.execute(
        select(Event).order_by(Event.created_at.desc()).offset(offset).limit(limit)
    )
    events = result.scalars().all()

    return {"items": [serialize_event(e) for e in events], "total": total}


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
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(select(Restaurant))
    total = len(count_result.scalars().all())

    result = await db.execute(
        select(Restaurant).order_by(Restaurant.created_at.desc()).offset(offset).limit(limit)
    )
    restaurants = result.scalars().all()
    return {"items": [serialize_restaurant(r) for r in restaurants], "total": total}


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
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(select(Course))
    total = len(count_result.scalars().all())

    result = await db.execute(
        select(Course).order_by(Course.created_at.desc()).offset(offset).limit(limit)
    )
    courses = result.scalars().all()
    return {"items": [serialize_course(c) for c in courses], "total": total}


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
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(select(Product))
    total = len(count_result.scalars().all())

    result = await db.execute(
        select(Product).order_by(Product.created_at.desc()).offset(offset).limit(limit)
    )
    products = result.scalars().all()
    return {"items": [serialize_product(p) for p in products], "total": total}


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
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    count_result = await db.execute(select(Guide))
    total = len(count_result.scalars().all())

    result = await db.execute(
        select(Guide).order_by(Guide.created_at.desc()).offset(offset).limit(limit)
    )
    guides = result.scalars().all()
    return {"items": [serialize_guide(g) for g in guides], "total": total}


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
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(Booking)
    if status:
        query = query.where(Booking.status == status)

    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    query = query.order_by(Booking.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    bookings = result.scalars().all()

    return {"items": [serialize_booking(b) for b in bookings], "total": total}


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


# ─────────────────────── Users (Admin) ───────────────────────

@router.get("/users")
async def admin_list_users(
    role: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(User)
    if role:
        query = query.where(User.role == role)

    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    query = query.order_by(User.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

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
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
        "total": total,
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
    language_code: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(UITranslation)
    if language_code:
        query = query.where(UITranslation.language_code == language_code)

    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    query = query.order_by(UITranslation.key).offset(offset).limit(limit)
    result = await db.execute(query)
    translations = result.scalars().all()

    return {
        "items": [
            {
                "id": t.id,
                "language_code": t.language_code,
                "key": t.key,
                "value": t.value,
            }
            for t in translations
        ],
        "total": total,
    }


@router.post("/translations")
async def admin_create_translation(
    data: UITranslationCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    # Check if key already exists for this language
    existing = await db.execute(
        select(UITranslation).where(
            UITranslation.language_code == data.language_code,
            UITranslation.key == data.key,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Translation key already exists for this language")

    translation = UITranslation(**data.model_dump())
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
async def admin_update_translation(
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
