from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.festival import Festival
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/festivals", tags=["Festivals"])


def serialize_festival(f, lang: str = "en") -> dict:
    return {
        "id": f.id,
        "name": get_multilingual_field(f, "name", lang),
        "description": get_multilingual_field(f, "description", lang),
        "category": f.category,
        "image_url": f.image_url,
        "images": f.images,
        "venue_name": f.venue_name,
        "address": f.address,
        "latitude": f.latitude,
        "longitude": f.longitude,
        "start_date": str(f.start_date) if f.start_date else None,
        "end_date": str(f.end_date) if f.end_date else None,
        "website_url": f.website_url,
        "is_active": f.is_active,
        "created_at": f.created_at.isoformat() if f.created_at else None,
        "updated_at": f.updated_at.isoformat() if f.updated_at else None,
    }


@router.get("/")
async def list_festivals(
    lang: str = Query("en"),
    category: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None, description="Filter: start_date >= this (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter: end_date <= this (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List festivals with optional date range and category filters."""
    query = select(Festival).where(Festival.is_active == True)

    if category:
        query = query.where(Festival.category == category)

    if start_date:
        try:
            start_d = date.fromisoformat(start_date)
            # Festivals that haven't ended before the start filter
            query = query.where(
                (Festival.end_date >= start_d) | (Festival.end_date == None)
            )
        except ValueError:
            pass

    if end_date:
        try:
            end_d = date.fromisoformat(end_date)
            # Festivals that start before or on the end filter
            query = query.where(
                (Festival.start_date <= end_d) | (Festival.start_date == None)
            )
        except ValueError:
            pass

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(Festival.start_date.asc().nullslast()).offset(offset).limit(per_page)
    result = await db.execute(query)
    festivals = result.scalars().all()

    return {
        "items": [serialize_festival(f, lang) for f in festivals],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{festival_id}")
async def get_festival(
    festival_id: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    """Get a single festival detail."""
    result = await db.execute(select(Festival).where(Festival.id == festival_id))
    festival = result.scalar_one_or_none()
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")

    return serialize_festival(festival, lang)
