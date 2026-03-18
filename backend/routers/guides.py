from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.guide import Guide, GuideAvailability
from models.event import EventGuide
from utils.helpers import serialize_guide

router = APIRouter(prefix="/api/v1/guides", tags=["Guides"])


@router.get("/")
async def list_guides(
    lang: str = Query("en"),
    event_id: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),  # price_asc, price_desc, name
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    if event_id:
        query = (
            select(Guide)
            .join(EventGuide, EventGuide.guide_id == Guide.id)
            .where(EventGuide.event_id == event_id)
            .where(Guide.status == "active")
        )
    else:
        query = select(Guide).where(Guide.status == "active")

    # Note: language and specialty filtering on JSON fields is limited in SQLite.
    # For production with PostgreSQL, use JSON operators.
    # Here we do basic filtering.

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Sorting
    if sort_by == "price_asc":
        query = query.order_by(Guide.price_per_hour_usd.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Guide.price_per_hour_usd.desc())
    elif sort_by == "name":
        query = query.order_by(Guide.name_en)
    else:
        query = query.order_by(Guide.created_at.desc())

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    guides = result.scalars().all()

    # Post-filter for language and specialty (JSON field filtering)
    filtered_guides = []
    for g in guides:
        if language and g.languages:
            lang_names = [l.get("language", "").lower() if isinstance(l, dict) else str(l).lower() for l in g.languages]
            if language.lower() not in lang_names:
                continue
        if specialty and g.specialties:
            if specialty.lower() not in [s.lower() for s in g.specialties]:
                continue
        if region and g.regions:
            if region.lower() not in [r.lower() for r in g.regions]:
                continue
        filtered_guides.append(g)

    return {
        "items": [serialize_guide(g, lang) for g in filtered_guides],
        "total": len(filtered_guides),
        "limit": limit,
        "offset": offset,
    }


@router.get("/{guide_id}")
async def get_guide(
    guide_id: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Guide).where(Guide.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    return serialize_guide(guide, lang)


@router.get("/{guide_id}/availability")
async def get_guide_availability(
    guide_id: str,
    db: AsyncSession = Depends(get_db),
):
    # Verify guide exists
    result = await db.execute(select(Guide).where(Guide.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    avail_result = await db.execute(
        select(GuideAvailability)
        .where(GuideAvailability.guide_id == guide_id)
        .order_by(GuideAvailability.date)
    )
    availability = avail_result.scalars().all()

    return {
        "guide_id": guide_id,
        "availability": [
            {
                "id": a.id,
                "date": str(a.date),
                "is_available": a.is_available,
            }
            for a in availability
        ],
    }
