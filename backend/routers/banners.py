from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.banner import RollingBanner
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/banners", tags=["Banners"])


@router.get("/")
async def list_banners(
    lang: str = Query("en"),
    event_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List active rolling banners, optionally filtered by event_id."""
    query = select(RollingBanner).where(RollingBanner.is_active == True)

    if event_id:
        # Show banners for this event + banners with no event (global)
        query = query.where(
            (RollingBanner.event_id == event_id) | (RollingBanner.event_id == None)
        )

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(RollingBanner.display_order).offset(offset).limit(per_page)
    result = await db.execute(query)
    banners = result.scalars().all()

    return {
        "items": [
            {
                "id": b.id,
                "title": get_multilingual_field(b, "title", lang),
                "subtitle": get_multilingual_field(b, "subtitle", lang),
                "image_url": b.image_url,
                "link_url": b.link_url,
                "display_order": b.display_order,
                "rolling_interval": b.rolling_interval,
                "transition_type": b.transition_type or "slide",
                "event_id": b.event_id,
                "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in banners
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }
