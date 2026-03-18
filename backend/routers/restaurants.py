from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.restaurant import Restaurant
from models.event import EventRestaurant
from utils.helpers import serialize_restaurant

router = APIRouter(prefix="/api/v1/restaurants", tags=["Restaurants"])


@router.get("/")
async def list_restaurants(
    lang: str = Query("en"),
    event_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    price_range: Optional[int] = Query(None, ge=1, le=4),
    sort_by: Optional[str] = Query(None),  # name, price_range, category
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    if event_id:
        query = (
            select(Restaurant)
            .join(EventRestaurant, EventRestaurant.restaurant_id == Restaurant.id)
            .where(EventRestaurant.event_id == event_id)
            .where(Restaurant.is_active == True)
        )
    else:
        query = select(Restaurant).where(Restaurant.is_active == True)

    if category:
        query = query.where(Restaurant.category == category)
    if price_range:
        query = query.where(Restaurant.price_range == price_range)

    # Sorting
    if sort_by == "price_range":
        query = query.order_by(Restaurant.price_range)
    elif sort_by == "name":
        query = query.order_by(Restaurant.name_en)
    elif sort_by == "category":
        query = query.order_by(Restaurant.category)
    else:
        query = query.order_by(Restaurant.created_at.desc())

    # Count
    count_query = select(Restaurant).where(Restaurant.is_active == True)
    if event_id:
        count_query = (
            select(Restaurant)
            .join(EventRestaurant, EventRestaurant.restaurant_id == Restaurant.id)
            .where(EventRestaurant.event_id == event_id)
            .where(Restaurant.is_active == True)
        )
    if category:
        count_query = count_query.where(Restaurant.category == category)
    if price_range:
        count_query = count_query.where(Restaurant.price_range == price_range)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    restaurants = result.scalars().all()

    return {
        "items": [serialize_restaurant(r, lang) for r in restaurants],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{restaurant_id}")
async def get_restaurant(
    restaurant_id: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return serialize_restaurant(restaurant, lang)
