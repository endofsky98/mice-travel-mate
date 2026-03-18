from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.living_guide import LivingGuideCategory, LivingGuideArticle
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/living-guide", tags=["Living Guide"])


@router.get("/categories")
async def list_categories(
    lang: str = Query("en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List living guide categories."""
    query = select(LivingGuideCategory).where(LivingGuideCategory.is_active == True)

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(LivingGuideCategory.display_order).offset(offset).limit(per_page)
    result = await db.execute(query)
    categories = result.scalars().all()

    return {
        "items": [
            {
                "id": c.id,
                "name": get_multilingual_field(c, "name", lang),
                "icon": c.icon,
                "display_order": c.display_order,
            }
            for c in categories
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/categories/{category_id}/articles")
async def list_articles(
    category_id: str,
    lang: str = Query("en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List articles for a specific category."""
    # Verify category exists
    cat_result = await db.execute(
        select(LivingGuideCategory).where(LivingGuideCategory.id == category_id)
    )
    category = cat_result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    query = select(LivingGuideArticle).where(
        LivingGuideArticle.category_id == category_id,
        LivingGuideArticle.is_active == True,
    )

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(LivingGuideArticle.display_order).offset(offset).limit(per_page)
    result = await db.execute(query)
    articles = result.scalars().all()

    return {
        "category": {
            "id": category.id,
            "name": get_multilingual_field(category, "name", lang),
            "icon": category.icon,
        },
        "items": [
            {
                "id": a.id,
                "category_id": a.category_id,
                "title": get_multilingual_field(a, "title", lang),
                "content": get_multilingual_field(a, "content", lang),
                "image_url": a.image_url,
                "display_order": a.display_order,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "updated_at": a.updated_at.isoformat() if a.updated_at else None,
            }
            for a in articles
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }
