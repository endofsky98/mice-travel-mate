import uuid
import math
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from pydantic import BaseModel, Field

from database import get_db
from models.restaurant import Restaurant
from models.course import Course, CourseSpot
from models.user import User
from auth.dependencies import get_current_user_optional
from utils.helpers import get_multilingual_field

router = APIRouter(prefix="/api/ai-courses", tags=["AI Courses"])


class CourseGenerateRequest(BaseModel):
    duration: str = Field(..., pattern="^(half_day|full_day|2day)$")
    interests: List[str] = Field(default_factory=list)  # food, history, nature, shopping, kpop, nightview
    budget: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    start_lat: Optional[float] = None
    start_lng: Optional[float] = None
    lang: str = Field("en")


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two GPS coordinates in km."""
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def estimate_travel_time(distance_km: float) -> int:
    """Estimate travel time in minutes based on distance."""
    if distance_km < 1:
        return 10  # Walking
    elif distance_km < 5:
        return 15  # Short taxi/bus
    elif distance_km < 15:
        return 30  # Subway
    elif distance_km < 30:
        return 45  # Longer subway
    else:
        return 60  # Long distance


@router.post("/generate")
async def generate_course(
    data: CourseGenerateRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """Generate an AI-recommended course based on user preferences."""
    lang = data.lang

    # Determine max spots and time budget
    duration_config = {
        "half_day": {"max_spots": 4, "total_minutes": 240, "max_distance_km": 20},
        "full_day": {"max_spots": 7, "total_minutes": 480, "max_distance_km": 50},
        "2day": {"max_spots": 12, "total_minutes": 960, "max_distance_km": 100},
    }
    config = duration_config[data.duration]

    # Budget mapping for price range filter
    budget_map = {
        "low": [1, 2],
        "medium": [2, 3],
        "high": [3, 4],
    }

    # Step 1: Find matching existing courses
    course_query = select(Course).where(Course.is_active == True)
    if data.duration in ("half_day", "full_day"):
        course_query = course_query.where(Course.duration_type == data.duration)

    course_query = course_query.limit(20)
    course_result = await db.execute(course_query)
    existing_courses = course_result.scalars().all()

    # Score existing courses by relevance
    scored_courses = []
    for course in existing_courses:
        score = 0
        if course.theme and data.interests:
            if course.theme in data.interests:
                score += 10
        if course.duration_type == data.duration:
            score += 5
        scored_courses.append((course, score))
    scored_courses.sort(key=lambda x: x[1], reverse=True)

    # Step 2: Gather candidate spots from best matching course
    candidate_spots = []
    if scored_courses:
        best_course = scored_courses[0][0]
        spots_result = await db.execute(
            select(CourseSpot)
            .where(CourseSpot.course_id == best_course.id)
            .order_by(CourseSpot.spot_order)
        )
        candidate_spots = list(spots_result.scalars().all())

    # Step 3: Find nearby restaurants based on interests and location
    restaurant_query = select(Restaurant).where(Restaurant.is_active == True)

    if data.budget and data.budget in budget_map:
        price_ranges = budget_map[data.budget]
        restaurant_query = restaurant_query.where(Restaurant.price_range.in_(price_ranges))

    if "food" in data.interests:
        restaurant_query = restaurant_query.limit(20)
    else:
        restaurant_query = restaurant_query.limit(10)

    rest_result = await db.execute(restaurant_query)
    restaurants = rest_result.scalars().all()

    # Score restaurants by proximity
    scored_restaurants = []
    for r in restaurants:
        score = 0
        if r.latitude and r.longitude and data.start_lat and data.start_lng:
            dist = haversine_distance(data.start_lat, data.start_lng, r.latitude, r.longitude)
            if dist <= config["max_distance_km"]:
                score += max(0, 20 - dist)  # Closer = higher score
        else:
            score += 5  # Default score if no coords

        if "food" in data.interests:
            score += 5
        scored_restaurants.append((r, score))
    scored_restaurants.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Build the optimal route
    route_spots = []
    total_time = 0
    last_lat = data.start_lat
    last_lng = data.start_lng

    # Add course spots
    for spot in candidate_spots[:config["max_spots"] - 1]:
        stay = spot.stay_duration_minutes or 30
        travel_time = 0
        distance = 0

        if last_lat and last_lng and spot.latitude and spot.longitude:
            distance = haversine_distance(last_lat, last_lng, spot.latitude, spot.longitude)
            travel_time = estimate_travel_time(distance)

        if total_time + travel_time + stay > config["total_minutes"]:
            break

        route_spots.append({
            "order": len(route_spots) + 1,
            "type": "spot",
            "name": get_multilingual_field(spot, "name", lang),
            "description": get_multilingual_field(spot, "description", lang),
            "latitude": spot.latitude,
            "longitude": spot.longitude,
            "stay_duration_minutes": stay,
            "travel_time_from_prev": travel_time,
            "distance_from_prev_km": round(distance, 1),
            "image_url": spot.image_url,
        })

        total_time += travel_time + stay
        if spot.latitude and spot.longitude:
            last_lat = spot.latitude
            last_lng = spot.longitude

    # Insert a restaurant recommendation
    if scored_restaurants and len(route_spots) < config["max_spots"]:
        best_restaurant = scored_restaurants[0][0]
        stay = 60  # 1 hour for a meal
        travel_time = 0
        distance = 0

        if last_lat and last_lng and best_restaurant.latitude and best_restaurant.longitude:
            distance = haversine_distance(
                last_lat, last_lng,
                best_restaurant.latitude, best_restaurant.longitude,
            )
            travel_time = estimate_travel_time(distance)

        if total_time + travel_time + stay <= config["total_minutes"]:
            route_spots.append({
                "order": len(route_spots) + 1,
                "type": "restaurant",
                "name": get_multilingual_field(best_restaurant, "name", lang),
                "description": get_multilingual_field(best_restaurant, "description", lang),
                "latitude": best_restaurant.latitude,
                "longitude": best_restaurant.longitude,
                "stay_duration_minutes": stay,
                "travel_time_from_prev": travel_time,
                "distance_from_prev_km": round(distance, 1),
                "image_url": best_restaurant.images[0] if best_restaurant.images else None,
                "restaurant_id": best_restaurant.id,
                "category": best_restaurant.category,
                "price_range": best_restaurant.price_range,
            })
            total_time += travel_time + stay
            if best_restaurant.latitude and best_restaurant.longitude:
                last_lat = best_restaurant.latitude
                last_lng = best_restaurant.longitude

    # Calculate total distance
    total_distance = sum(s.get("distance_from_prev_km", 0) for s in route_spots)

    # Build timeline
    timeline = []
    current_minutes = 540  # Start at 9:00 AM
    for spot in route_spots:
        current_minutes += spot.get("travel_time_from_prev", 0)
        arrival_time = f"{current_minutes // 60:02d}:{current_minutes % 60:02d}"
        current_minutes += spot.get("stay_duration_minutes", 30)
        end_time = f"{current_minutes // 60:02d}:{current_minutes % 60:02d}"

        timeline.append({
            "order": spot["order"],
            "name": spot["name"],
            "travel_from_prev": f"{spot.get('travel_time_from_prev', 0)} min",
            "arrival": arrival_time,
            "departure": end_time,
            "stay_duration": f"{spot.get('stay_duration_minutes', 30)} min",
        })

    # Map data for frontend rendering
    map_data = {
        "center_lat": data.start_lat or (route_spots[0]["latitude"] if route_spots else 37.5665),
        "center_lng": data.start_lng or (route_spots[0]["longitude"] if route_spots else 126.9780),
        "zoom": 12 if data.duration == "half_day" else 10,
        "markers": [
            {
                "order": s["order"],
                "lat": s["latitude"],
                "lng": s["longitude"],
                "name": s["name"],
                "type": s["type"],
            }
            for s in route_spots
            if s.get("latitude") and s.get("longitude")
        ],
    }

    return {
        "generated_course": {
            "duration": data.duration,
            "interests": data.interests,
            "budget": data.budget,
            "total_spots": len(route_spots),
            "total_duration_minutes": total_time,
            "total_distance_km": round(total_distance, 1),
            "spots": route_spots,
            "timeline": timeline,
            "map_data": map_data,
            "based_on_course": (
                {
                    "id": scored_courses[0][0].id,
                    "name": get_multilingual_field(scored_courses[0][0], "name", lang),
                }
                if scored_courses
                else None
            ),
        },
    }
