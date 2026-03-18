import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

from database import get_db
from models.restaurant import Restaurant
from models.course import Course
from models.product import Product
from models.guide import Guide
from models.festival import Festival
from models.analytics import SearchLog
from models.user import User
from auth.dependencies import get_current_user_optional
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/")
async def unified_search(
    q: str = Query(..., min_length=1, max_length=200),
    lang: str = Query("en"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """Search across restaurants, courses, products, guides, and festivals."""
    search_term = f"%{q}%"
    results = []

    # Search Restaurants
    restaurant_query = select(Restaurant).where(
        Restaurant.is_active == True,
        or_(
            Restaurant.name_en.ilike(search_term),
            Restaurant.name_ko.ilike(search_term),
            Restaurant.name_ja.ilike(search_term),
            Restaurant.name_zh_cn.ilike(search_term),
            Restaurant.description_en.ilike(search_term),
            Restaurant.description_ko.ilike(search_term),
            Restaurant.category.ilike(search_term),
            Restaurant.address.ilike(search_term),
        ),
    ).limit(10)
    rest_result = await db.execute(restaurant_query)
    for r in rest_result.scalars().all():
        results.append({
            "type": "restaurant",
            "id": r.id,
            "name": get_multilingual_field(r, "name", lang),
            "description": get_multilingual_field(r, "description", lang),
            "image_url": r.images[0] if r.images else None,
            "category": r.category,
            "latitude": r.latitude,
            "longitude": r.longitude,
        })

    # Search Courses
    course_query = select(Course).where(
        Course.is_active == True,
        or_(
            Course.name_en.ilike(search_term),
            Course.name_ko.ilike(search_term),
            Course.name_ja.ilike(search_term),
            Course.name_zh_cn.ilike(search_term),
            Course.description_en.ilike(search_term),
            Course.description_ko.ilike(search_term),
            Course.theme.ilike(search_term),
            Course.region.ilike(search_term),
        ),
    ).limit(10)
    course_result = await db.execute(course_query)
    for c in course_result.scalars().all():
        results.append({
            "type": "course",
            "id": c.id,
            "name": get_multilingual_field(c, "name", lang),
            "description": get_multilingual_field(c, "description", lang),
            "image_url": c.image_url,
            "category": c.theme,
        })

    # Search Products
    product_query = select(Product).where(
        Product.status == "active",
        or_(
            Product.name_en.ilike(search_term),
            Product.name_ko.ilike(search_term),
            Product.name_ja.ilike(search_term),
            Product.name_zh_cn.ilike(search_term),
            Product.description_en.ilike(search_term),
            Product.description_ko.ilike(search_term),
            Product.category.ilike(search_term),
            Product.region.ilike(search_term),
        ),
    ).limit(10)
    prod_result = await db.execute(product_query)
    for p in prod_result.scalars().all():
        results.append({
            "type": "product",
            "id": p.id,
            "name": get_multilingual_field(p, "name", lang),
            "description": get_multilingual_field(p, "description", lang),
            "image_url": p.images[0] if p.images else None,
            "category": p.category,
            "price_usd": float(p.price_usd) if p.price_usd else None,
        })

    # Search Guides
    guide_query = select(Guide).where(
        Guide.status == "active",
        or_(
            Guide.name_en.ilike(search_term),
            Guide.name_ko.ilike(search_term),
            Guide.name_ja.ilike(search_term),
            Guide.name_zh_cn.ilike(search_term),
            Guide.bio_en.ilike(search_term),
            Guide.bio_ko.ilike(search_term),
            Guide.services_en.ilike(search_term),
            Guide.services_ko.ilike(search_term),
        ),
    ).limit(10)
    guide_result = await db.execute(guide_query)
    for g in guide_result.scalars().all():
        results.append({
            "type": "guide",
            "id": g.id,
            "name": get_multilingual_field(g, "name", lang),
            "description": get_multilingual_field(g, "bio", lang),
            "image_url": g.profile_image_url,
            "category": None,
        })

    # Search Festivals
    festival_query = select(Festival).where(
        Festival.is_active == True,
        or_(
            Festival.name_en.ilike(search_term),
            Festival.name_ko.ilike(search_term),
            Festival.name_ja.ilike(search_term),
            Festival.name_zh_cn.ilike(search_term),
            Festival.description_en.ilike(search_term),
            Festival.description_ko.ilike(search_term),
            Festival.venue_name.ilike(search_term),
            Festival.category.ilike(search_term),
        ),
    ).limit(10)
    fest_result = await db.execute(festival_query)
    for f in fest_result.scalars().all():
        results.append({
            "type": "festival",
            "id": f.id,
            "name": get_multilingual_field(f, "name", lang),
            "description": get_multilingual_field(f, "description", lang),
            "image_url": f.image_url,
            "category": f.category,
            "start_date": str(f.start_date) if f.start_date else None,
            "end_date": str(f.end_date) if f.end_date else None,
        })

    # Log the search query
    search_log = SearchLog(
        id=str(uuid.uuid4()),
        query=q,
        language=lang,
        result_count=len(results),
        user_id=current_user.id if current_user else None,
    )
    db.add(search_log)
    await db.flush()

    # Apply pagination to combined results
    total = len(results)
    offset = (page - 1) * per_page
    paginated_results = results[offset:offset + per_page]

    return {
        "query": q,
        "items": paginated_results,
        "total": total,
        "page": page,
        "per_page": per_page,
    }
