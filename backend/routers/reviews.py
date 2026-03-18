import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from pydantic import BaseModel, Field
from typing import List

from database import get_db
from models.review import Review
from models.user import User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


class ReviewCreate(BaseModel):
    target_type: str = Field(..., pattern="^(restaurant|course|product|guide)$")
    target_id: str
    rating: int = Field(..., ge=1, le=5)
    content: str = Field(..., min_length=1, max_length=2000)
    images: Optional[List[str]] = Field(None, max_length=5)


class ReviewReport(BaseModel):
    reason: str = Field(..., max_length=50)


@router.get("/")
async def list_reviews(
    target_type: str = Query(..., pattern="^(restaurant|course|product|guide)$"),
    target_id: str = Query(...),
    status: Optional[str] = Query("approved"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List reviews for a specific target (restaurant, course, product, guide)."""
    query = select(Review).where(
        Review.target_type == target_type,
        Review.target_id == target_id,
    )
    if status:
        query = query.where(Review.status == status)

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(Review.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    reviews = result.scalars().all()

    # Fetch user names for each review
    user_ids = list({r.user_id for r in reviews})
    users_map = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        for u in users_result.scalars().all():
            users_map[u.id] = u

    return {
        "items": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "user_name": users_map.get(r.user_id, None) and users_map[r.user_id].name,
                "target_type": r.target_type,
                "target_id": r.target_id,
                "rating": r.rating,
                "content": r.content,
                "images": r.images,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in reviews
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.post("/")
async def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new review (auth required)."""
    # Check if user already reviewed this target
    existing = await db.execute(
        select(Review).where(
            Review.user_id == current_user.id,
            Review.target_type == data.target_type,
            Review.target_id == data.target_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You have already reviewed this item")

    review = Review(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        target_type=data.target_type,
        target_id=data.target_id,
        rating=data.rating,
        content=data.content,
        images=data.images,
        status="approved",  # Auto-approve for now
    )
    db.add(review)
    await db.flush()
    await db.refresh(review)

    return {
        "id": review.id,
        "user_id": review.user_id,
        "user_name": current_user.name,
        "target_type": review.target_type,
        "target_id": review.target_id,
        "rating": review.rating,
        "content": review.content,
        "images": review.images,
        "status": review.status,
        "created_at": review.created_at.isoformat() if review.created_at else None,
    }


@router.put("/{review_id}/report")
async def report_review(
    review_id: str,
    data: ReviewReport,
    db: AsyncSession = Depends(get_db),
):
    """Report a review."""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.is_reported = True
    review.report_reason = data.reason
    review.report_count = (review.report_count or 0) + 1
    review.updated_at = datetime.utcnow()

    # Auto-hide if reported too many times
    if review.report_count >= 3:
        review.status = "deleted"

    await db.flush()
    await db.refresh(review)

    return {"message": "Review reported", "report_count": review.report_count}


@router.get("/stats")
async def review_stats(
    target_type: str = Query(..., pattern="^(restaurant|course|product|guide)$"),
    target_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Get average rating and distribution for a target."""
    base_query = select(Review).where(
        Review.target_type == target_type,
        Review.target_id == target_id,
        Review.status == "approved",
    )

    # Average rating
    avg_result = await db.execute(
        select(func.avg(Review.rating)).where(
            Review.target_type == target_type,
            Review.target_id == target_id,
            Review.status == "approved",
        )
    )
    avg_rating = avg_result.scalar()

    # Total count
    count_result = await db.execute(
        select(func.count(Review.id)).where(
            Review.target_type == target_type,
            Review.target_id == target_id,
            Review.status == "approved",
        )
    )
    total_count = count_result.scalar()

    # Distribution by rating
    distribution = {}
    for star in range(1, 6):
        star_result = await db.execute(
            select(func.count(Review.id)).where(
                Review.target_type == target_type,
                Review.target_id == target_id,
                Review.status == "approved",
                Review.rating == star,
            )
        )
        distribution[str(star)] = star_result.scalar() or 0

    return {
        "target_type": target_type,
        "target_id": target_id,
        "avg_rating": round(float(avg_rating), 2) if avg_rating else 0,
        "total_count": total_count or 0,
        "distribution": distribution,
    }
