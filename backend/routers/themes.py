from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.theme import Theme, ThemeSpot
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/themes", tags=["Themes"])


@router.get("/")
async def list_themes(
    lang: str = Query("en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all active themes."""
    query = select(Theme).where(Theme.is_active == True)

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(Theme.display_order).offset(offset).limit(per_page)
    result = await db.execute(query)
    themes = result.scalars().all()

    return {
        "items": [
            {
                "id": t.id,
                "name": get_multilingual_field(t, "name", lang),
                "description": get_multilingual_field(t, "description", lang),
                "icon": t.icon,
                "color": t.color,
                "display_order": t.display_order,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in themes
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{theme_id}/spots")
async def list_theme_spots(
    theme_id: str,
    lang: str = Query("en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List spots for a specific theme."""
    # Verify theme exists
    theme_result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = theme_result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    query = select(ThemeSpot).where(ThemeSpot.theme_id == theme_id)

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(ThemeSpot.display_order).offset(offset).limit(per_page)
    result = await db.execute(query)
    spots = result.scalars().all()

    # Resolve target details for each spot
    items = []
    for spot in spots:
        spot_data = {
            "id": spot.id,
            "theme_id": spot.theme_id,
            "target_type": spot.target_type,
            "target_id": spot.target_id,
            "display_order": spot.display_order,
            "target_detail": None,
        }

        # Lazy-load target details based on type
        if spot.target_type == "restaurant":
            from models.restaurant import Restaurant
            target_result = await db.execute(
                select(Restaurant).where(Restaurant.id == spot.target_id)
            )
            target = target_result.scalar_one_or_none()
            if target:
                spot_data["target_detail"] = {
                    "name": get_multilingual_field(target, "name", lang),
                    "latitude": target.latitude,
                    "longitude": target.longitude,
                    "image_url": target.images[0] if target.images else None,
                    "category": target.category,
                }
        elif spot.target_type == "course_spot":
            from models.course import CourseSpot
            target_result = await db.execute(
                select(CourseSpot).where(CourseSpot.id == spot.target_id)
            )
            target = target_result.scalar_one_or_none()
            if target:
                spot_data["target_detail"] = {
                    "name": get_multilingual_field(target, "name", lang),
                    "latitude": target.latitude,
                    "longitude": target.longitude,
                    "image_url": target.image_url,
                }
        elif spot.target_type == "festival":
            from models.festival import Festival
            target_result = await db.execute(
                select(Festival).where(Festival.id == spot.target_id)
            )
            target = target_result.scalar_one_or_none()
            if target:
                spot_data["target_detail"] = {
                    "name": get_multilingual_field(target, "name", lang),
                    "latitude": target.latitude,
                    "longitude": target.longitude,
                    "image_url": target.image_url,
                    "start_date": str(target.start_date) if target.start_date else None,
                    "end_date": str(target.end_date) if target.end_date else None,
                }

        items.append(spot_data)

    return {
        "theme": {
            "id": theme.id,
            "name": get_multilingual_field(theme, "name", lang),
            "description": get_multilingual_field(theme, "description", lang),
            "icon": theme.icon,
            "color": theme.color,
        },
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
    }
