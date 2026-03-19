from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.course import Course, CourseSpot, CourseSpotTransition
from models.event import EventCourse
from utils.helpers import serialize_course, serialize_course_spot, serialize_course_spot_transition

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get("/")
async def list_courses(
    lang: str = Query("en"),
    event_id: Optional[str] = Query(None),
    duration_type: Optional[str] = Query(None),
    theme: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    if event_id:
        query = (
            select(Course)
            .join(EventCourse, EventCourse.course_id == Course.id)
            .where(EventCourse.event_id == event_id)
            .where(Course.is_active == True)
        )
    else:
        query = select(Course).where(Course.is_active == True)

    if duration_type:
        query = query.where(Course.duration_type == duration_type)
    if theme:
        query = query.where(Course.theme == theme)
    if region:
        query = query.where(Course.region == region)
    if difficulty:
        query = query.where(Course.difficulty == difficulty)

    # Count
    count_query = query
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    query = query.order_by(Course.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    courses = result.scalars().all()

    return {
        "items": [serialize_course(c, lang) for c in courses],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{course_id}")
async def get_course(
    course_id: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Get spots
    spots_result = await db.execute(
        select(CourseSpot)
        .where(CourseSpot.course_id == course_id)
        .order_by(CourseSpot.spot_order)
    )
    spots = spots_result.scalars().all()

    # Get transitions
    transitions_result = await db.execute(
        select(CourseSpotTransition)
        .where(CourseSpotTransition.course_id == course_id)
    )
    transitions = transitions_result.scalars().all()

    course_data = serialize_course(course, lang)
    course_data["spots"] = [serialize_course_spot(s, lang) for s in spots]
    course_data["transitions"] = [serialize_course_spot_transition(t) for t in transitions]

    return course_data
