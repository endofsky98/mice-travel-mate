from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.product import Product, ProductInventory
from models.event import EventProduct
from utils.helpers import serialize_product

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/")
async def list_products(
    lang: str = Query("en"),
    event_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    duration_min: Optional[float] = Query(None),
    duration_max: Optional[float] = Query(None),
    region: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),  # price_asc, price_desc, duration, name
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    if event_id:
        query = (
            select(Product)
            .join(EventProduct, EventProduct.product_id == Product.id)
            .where(EventProduct.event_id == event_id)
            .where(Product.status == "active")
        )
    else:
        query = select(Product).where(Product.status == "active")

    if category:
        query = query.where(Product.category == category)
    if min_price is not None:
        query = query.where(Product.price_usd >= min_price)
    if max_price is not None:
        query = query.where(Product.price_usd <= max_price)
    if duration_min is not None:
        query = query.where(Product.duration_hours >= duration_min)
    if duration_max is not None:
        query = query.where(Product.duration_hours <= duration_max)
    if region:
        query = query.where(Product.region == region)

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Sorting
    if sort_by == "price_asc":
        query = query.order_by(Product.price_usd.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price_usd.desc())
    elif sort_by == "duration":
        query = query.order_by(Product.duration_hours)
    elif sort_by == "name":
        query = query.order_by(Product.name_en)
    else:
        query = query.order_by(Product.created_at.desc())

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()

    return {
        "items": [serialize_product(p, lang) for p in products],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{product_id}")
async def get_product(
    product_id: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get inventory
    inv_result = await db.execute(
        select(ProductInventory)
        .where(ProductInventory.product_id == product_id)
        .order_by(ProductInventory.date)
    )
    inventory = inv_result.scalars().all()

    product_data = serialize_product(product, lang)
    product_data["inventory"] = [
        {
            "id": inv.id,
            "date": str(inv.date),
            "total_slots": inv.total_slots,
            "booked_slots": inv.booked_slots,
            "available_slots": inv.total_slots - inv.booked_slots,
        }
        for inv in inventory
    ]

    return product_data
