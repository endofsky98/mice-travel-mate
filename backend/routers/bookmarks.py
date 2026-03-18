from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional

from database import get_db
from models.user import User, Bookmark
from schemas.user import BookmarkCreate, BookmarkResponse
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/bookmarks", tags=["Bookmarks"])

VALID_TARGET_TYPES = ["restaurant", "course", "product", "guide"]


@router.post("/", response_model=BookmarkResponse)
async def add_bookmark(
    data: BookmarkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.target_type not in VALID_TARGET_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid target_type. Must be one of: {VALID_TARGET_TYPES}")

    # Check if bookmark already exists
    result = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.user_id == current_user.id,
                Bookmark.target_type == data.target_type,
                Bookmark.target_id == data.target_id,
            )
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return BookmarkResponse(
            id=existing.id,
            user_id=existing.user_id,
            target_type=existing.target_type,
            target_id=existing.target_id,
            created_at=existing.created_at,
        )

    bookmark = Bookmark(
        user_id=current_user.id,
        target_type=data.target_type,
        target_id=data.target_id,
    )
    db.add(bookmark)
    await db.flush()
    await db.refresh(bookmark)

    return BookmarkResponse(
        id=bookmark.id,
        user_id=bookmark.user_id,
        target_type=bookmark.target_type,
        target_id=bookmark.target_id,
        created_at=bookmark.created_at,
    )


@router.delete("/{target_type}/{target_id}")
async def remove_bookmark(
    target_type: str,
    target_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.user_id == current_user.id,
                Bookmark.target_type == target_type,
                Bookmark.target_id == target_id,
            )
        )
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    await db.delete(bookmark)
    await db.flush()

    return {"message": "Bookmark removed"}


@router.get("/")
async def list_bookmarks(
    target_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Bookmark).where(Bookmark.user_id == current_user.id)
    if target_type:
        query = query.where(Bookmark.target_type == target_type)
    query = query.order_by(Bookmark.created_at.desc())

    result = await db.execute(query)
    bookmarks = result.scalars().all()

    return {
        "items": [
            {
                "id": b.id,
                "user_id": b.user_id,
                "target_type": b.target_type,
                "target_id": b.target_id,
                "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in bookmarks
        ]
    }
