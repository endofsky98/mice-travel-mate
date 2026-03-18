import uuid
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from pydantic import BaseModel

from database import get_db
from models.analytics import VisitorLog, ContentView, SearchLog
from models.user import User
from auth.dependencies import get_current_admin, get_current_user_optional

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class VisitLogRequest(BaseModel):
    session_id: Optional[str] = None
    page_path: Optional[str] = None
    referrer: Optional[str] = None
    event_slug: Optional[str] = None
    language: Optional[str] = None
    nationality: Optional[str] = None


class ContentViewRequest(BaseModel):
    target_type: str  # restaurant, course, product, guide
    target_id: str
    session_id: Optional[str] = None


@router.post("/visit")
async def log_visit(
    data: VisitLogRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """Log a visitor hit."""
    # Extract user agent and IP
    user_agent = request.headers.get("user-agent", "")
    ip_address = request.client.host if request.client else None

    visitor = VisitorLog(
        id=str(uuid.uuid4()),
        session_id=data.session_id,
        user_id=current_user.id if current_user else None,
        page_path=data.page_path,
        referrer=data.referrer,
        event_slug=data.event_slug,
        language=data.language,
        nationality=data.nationality,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    db.add(visitor)
    await db.flush()

    return {"message": "Visit logged", "id": visitor.id}


@router.post("/view")
async def log_content_view(
    data: ContentViewRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """Log a content view."""
    view = ContentView(
        id=str(uuid.uuid4()),
        target_type=data.target_type,
        target_id=data.target_id,
        user_id=current_user.id if current_user else None,
        session_id=data.session_id,
    )
    db.add(view)
    await db.flush()

    return {"message": "View logged", "id": view.id}


@router.get("/stats/visitors")
async def visitor_stats(
    days: int = Query(30, ge=1, le=365),
    event_slug: Optional[str] = Query(None),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get visitor statistics (admin only)."""
    since = datetime.utcnow() - timedelta(days=days)

    base_filter = [VisitorLog.created_at >= since]
    if event_slug:
        base_filter.append(VisitorLog.event_slug == event_slug)

    # Total visitors
    total_result = await db.execute(
        select(func.count(VisitorLog.id)).where(*base_filter)
    )
    total_visits = total_result.scalar() or 0

    # Unique sessions
    unique_result = await db.execute(
        select(func.count(func.distinct(VisitorLog.session_id))).where(*base_filter)
    )
    unique_sessions = unique_result.scalar() or 0

    # By language
    lang_result = await db.execute(
        select(
            VisitorLog.language,
            func.count(VisitorLog.id),
        )
        .where(*base_filter)
        .group_by(VisitorLog.language)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(20)
    )
    by_language = [
        {"language": row[0] or "unknown", "count": row[1]}
        for row in lang_result.all()
    ]

    # By nationality
    nat_result = await db.execute(
        select(
            VisitorLog.nationality,
            func.count(VisitorLog.id),
        )
        .where(*base_filter)
        .group_by(VisitorLog.nationality)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(20)
    )
    by_nationality = [
        {"nationality": row[0] or "unknown", "count": row[1]}
        for row in nat_result.all()
    ]

    # Top pages
    page_result = await db.execute(
        select(
            VisitorLog.page_path,
            func.count(VisitorLog.id),
        )
        .where(*base_filter)
        .group_by(VisitorLog.page_path)
        .order_by(func.count(VisitorLog.id).desc())
        .limit(20)
    )
    top_pages = [
        {"page": row[0] or "/", "count": row[1]}
        for row in page_result.all()
    ]

    return {
        "period_days": days,
        "total_visits": total_visits,
        "unique_sessions": unique_sessions,
        "by_language": by_language,
        "by_nationality": by_nationality,
        "top_pages": top_pages,
    }


@router.get("/stats/searches")
async def search_stats(
    days: int = Query(30, ge=1, le=365),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get search statistics (admin only)."""
    since = datetime.utcnow() - timedelta(days=days)

    # Total searches
    total_result = await db.execute(
        select(func.count(SearchLog.id)).where(SearchLog.created_at >= since)
    )
    total_searches = total_result.scalar() or 0

    # Top search queries
    top_queries_result = await db.execute(
        select(
            SearchLog.query,
            func.count(SearchLog.id).label("count"),
            func.avg(SearchLog.result_count).label("avg_results"),
        )
        .where(SearchLog.created_at >= since)
        .group_by(SearchLog.query)
        .order_by(func.count(SearchLog.id).desc())
        .limit(30)
    )
    top_queries = [
        {
            "query": row[0],
            "count": row[1],
            "avg_results": round(float(row[2]), 1) if row[2] else 0,
        }
        for row in top_queries_result.all()
    ]

    # Searches with zero results
    zero_result = await db.execute(
        select(
            SearchLog.query,
            func.count(SearchLog.id).label("count"),
        )
        .where(
            SearchLog.created_at >= since,
            SearchLog.result_count == 0,
        )
        .group_by(SearchLog.query)
        .order_by(func.count(SearchLog.id).desc())
        .limit(20)
    )
    zero_result_queries = [
        {"query": row[0], "count": row[1]}
        for row in zero_result.all()
    ]

    # By language
    lang_result = await db.execute(
        select(
            SearchLog.language,
            func.count(SearchLog.id),
        )
        .where(SearchLog.created_at >= since)
        .group_by(SearchLog.language)
        .order_by(func.count(SearchLog.id).desc())
    )
    by_language = [
        {"language": row[0] or "unknown", "count": row[1]}
        for row in lang_result.all()
    ]

    return {
        "period_days": days,
        "total_searches": total_searches,
        "top_queries": top_queries,
        "zero_result_queries": zero_result_queries,
        "by_language": by_language,
    }


@router.get("/stats/content")
async def content_stats(
    days: int = Query(30, ge=1, le=365),
    target_type: Optional[str] = Query(None),
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get content view statistics (admin only)."""
    since = datetime.utcnow() - timedelta(days=days)

    base_filter = [ContentView.created_at >= since]
    if target_type:
        base_filter.append(ContentView.target_type == target_type)

    # Total views
    total_result = await db.execute(
        select(func.count(ContentView.id)).where(*base_filter)
    )
    total_views = total_result.scalar() or 0

    # Views by type
    type_result = await db.execute(
        select(
            ContentView.target_type,
            func.count(ContentView.id),
        )
        .where(*base_filter)
        .group_by(ContentView.target_type)
        .order_by(func.count(ContentView.id).desc())
    )
    by_type = [
        {"type": row[0], "count": row[1]}
        for row in type_result.all()
    ]

    # Top viewed items
    top_items_result = await db.execute(
        select(
            ContentView.target_type,
            ContentView.target_id,
            func.count(ContentView.id).label("view_count"),
        )
        .where(*base_filter)
        .group_by(ContentView.target_type, ContentView.target_id)
        .order_by(func.count(ContentView.id).desc())
        .limit(20)
    )
    top_items = [
        {
            "target_type": row[0],
            "target_id": row[1],
            "view_count": row[2],
        }
        for row in top_items_result.all()
    ]

    return {
        "period_days": days,
        "total_views": total_views,
        "by_type": by_type,
        "top_items": top_items,
    }
