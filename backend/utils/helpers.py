from datetime import datetime
from typing import Any, Optional


SUPPORTED_LANGUAGES = ["en", "ko", "zh_cn", "zh_tw", "ja", "es"]
LANGUAGE_CODE_MAP = {
    "en": "en",
    "ko": "ko",
    "zh-CN": "zh_cn",
    "zh-TW": "zh_tw",
    "zh_cn": "zh_cn",
    "zh_tw": "zh_tw",
    "ja": "ja",
    "es": "es",
}


def normalize_lang(lang: str) -> str:
    """Normalize language code to match database field suffix."""
    return LANGUAGE_CODE_MAP.get(lang, "en")


def get_multilingual_field(obj: Any, field_prefix: str, lang: str = "en") -> Optional[str]:
    """
    Get a multilingual field from an object based on language code.
    Falls back to English if the requested language field is empty.
    """
    norm_lang = normalize_lang(lang)
    value = getattr(obj, f"{field_prefix}_{norm_lang}", None)
    if value:
        return value
    # Fallback to English
    return getattr(obj, f"{field_prefix}_en", None)


def get_multilingual_json_field(obj: Any, field_prefix: str, lang: str = "en") -> Any:
    """
    Get a multilingual JSON field from an object based on language code.
    Falls back to English if the requested language field is empty.
    """
    norm_lang = normalize_lang(lang)
    value = getattr(obj, f"{field_prefix}_{norm_lang}", None)
    if value is not None:
        return value
    return getattr(obj, f"{field_prefix}_en", None)


def build_multilingual_dict(obj: Any, field_prefix: str, lang: str = "en") -> dict:
    """Build a dict with a single 'name'/'description' etc. field based on language."""
    return get_multilingual_field(obj, field_prefix, lang)


def serialize_event(event, lang: str = "en") -> dict:
    return {
        "id": event.id,
        "slug": event.slug,
        "name": get_multilingual_field(event, "name", lang),
        "description": get_multilingual_field(event, "description", lang),
        "venue_name": event.venue_name,
        "venue_address": event.venue_address,
        "latitude": event.latitude,
        "longitude": event.longitude,
        "start_date": str(event.start_date) if event.start_date else None,
        "end_date": str(event.end_date) if event.end_date else None,
        "banner_image_url": event.banner_image_url,
        "is_active": event.is_active,
        "created_at": event.created_at.isoformat() if event.created_at else None,
        "updated_at": event.updated_at.isoformat() if event.updated_at else None,
    }


def serialize_restaurant(restaurant, lang: str = "en") -> dict:
    return {
        "id": restaurant.id,
        "name": get_multilingual_field(restaurant, "name", lang),
        "description": get_multilingual_field(restaurant, "description", lang),
        "category": restaurant.category,
        "price_range": restaurant.price_range,
        "address": restaurant.address,
        "latitude": restaurant.latitude,
        "longitude": restaurant.longitude,
        "phone": restaurant.phone,
        "opening_hours": restaurant.opening_hours,
        "menu_highlights": restaurant.menu_highlights,
        "images": restaurant.images,
        "is_active": restaurant.is_active,
        "created_at": restaurant.created_at.isoformat() if restaurant.created_at else None,
        "updated_at": restaurant.updated_at.isoformat() if restaurant.updated_at else None,
    }


def serialize_course(course, lang: str = "en") -> dict:
    return {
        "id": course.id,
        "name": get_multilingual_field(course, "name", lang),
        "description": get_multilingual_field(course, "description", lang),
        "duration_type": course.duration_type,
        "theme": course.theme,
        "region": course.region,
        "difficulty": course.difficulty,
        "total_duration_minutes": course.total_duration_minutes,
        "total_distance_km": course.total_distance_km,
        "estimated_transport_cost": course.estimated_transport_cost,
        "image_url": course.image_url,
        "is_active": course.is_active,
        "created_at": course.created_at.isoformat() if course.created_at else None,
        "updated_at": course.updated_at.isoformat() if course.updated_at else None,
    }


def serialize_course_spot(spot, lang: str = "en") -> dict:
    return {
        "id": spot.id,
        "course_id": spot.course_id,
        "spot_order": spot.spot_order,
        "name": get_multilingual_field(spot, "name", lang),
        "description": get_multilingual_field(spot, "description", lang),
        "latitude": spot.latitude,
        "longitude": spot.longitude,
        "stay_duration_minutes": spot.stay_duration_minutes,
        "image_url": spot.image_url,
        "restaurant_id": spot.restaurant_id,
    }


def serialize_course_spot_transition(transition) -> dict:
    return {
        "id": transition.id,
        "course_id": transition.course_id,
        "from_spot_id": transition.from_spot_id,
        "to_spot_id": transition.to_spot_id,
        "transport_mode": transition.transport_mode,
        "duration_minutes": transition.duration_minutes,
        "distance_km": transition.distance_km,
        "route_polyline": transition.route_polyline,
    }


def serialize_transport_route(route, lang: str = "en") -> dict:
    return {
        "id": route.id,
        "from_name": get_multilingual_field(route, "from_name", lang),
        "to_name": get_multilingual_field(route, "to_name", lang),
        "from_latitude": route.from_latitude,
        "from_longitude": route.from_longitude,
        "to_latitude": route.to_latitude,
        "to_longitude": route.to_longitude,
        "transport_modes": route.transport_modes,
        "route_polyline": route.route_polyline,
        "is_active": route.is_active,
    }


def serialize_transport_tip(tip, lang: str = "en") -> dict:
    return {
        "id": tip.id,
        "title": get_multilingual_field(tip, "title", lang),
        "content": get_multilingual_field(tip, "content", lang),
        "category": tip.category,
        "icon": tip.icon,
        "display_order": tip.display_order,
        "is_active": tip.is_active,
    }


def serialize_product(product, lang: str = "en") -> dict:
    return {
        "id": product.id,
        "name": get_multilingual_field(product, "name", lang),
        "description": get_multilingual_field(product, "description", lang),
        "category": product.category,
        "price_usd": float(product.price_usd) if product.price_usd else None,
        "duration_hours": product.duration_hours,
        "region": product.region,
        "min_participants": product.min_participants,
        "max_participants": product.max_participants,
        "includes": get_multilingual_json_field(product, "includes", lang),
        "excludes": get_multilingual_json_field(product, "excludes", lang),
        "itinerary": product.itinerary,
        "meeting_point": product.meeting_point,
        "meeting_point_lat": product.meeting_point_lat,
        "meeting_point_lng": product.meeting_point_lng,
        "dismissal_point": product.dismissal_point,
        "cancellation_policy": get_multilingual_field(product, "cancellation_policy", lang),
        "images": product.images,
        "status": product.status,
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None,
    }


def serialize_guide(guide, lang: str = "en") -> dict:
    return {
        "id": guide.id,
        "name": get_multilingual_field(guide, "name", lang),
        "bio": get_multilingual_field(guide, "bio", lang),
        "profile_image_url": guide.profile_image_url,
        "languages": guide.languages,
        "specialties": guide.specialties,
        "regions": guide.regions,
        "price_per_hour_usd": float(guide.price_per_hour_usd) if guide.price_per_hour_usd else None,
        "price_half_day_usd": float(guide.price_half_day_usd) if guide.price_half_day_usd else None,
        "price_full_day_usd": float(guide.price_full_day_usd) if guide.price_full_day_usd else None,
        "services": get_multilingual_field(guide, "services", lang),
        "status": guide.status,
        "created_at": guide.created_at.isoformat() if guide.created_at else None,
        "updated_at": guide.updated_at.isoformat() if guide.updated_at else None,
    }


def serialize_booking(booking) -> dict:
    booking_date_str = str(booking.booking_date) if booking.booking_date else None
    total_amount = float(booking.total_amount_usd) if booking.total_amount_usd else None
    return {
        "id": booking.id,
        "booking_number": booking.booking_number,
        "user_id": booking.user_id,
        "booking_type": booking.booking_type,
        "type": booking.booking_type,
        "product_id": booking.product_id,
        "guide_id": booking.guide_id,
        "event_id": booking.event_id,
        "booking_date": booking_date_str,
        "date": booking_date_str,
        "num_participants": booking.num_participants,
        "participants": booking.num_participants,
        "options": booking.options,
        "guest_name": booking.guest_name,
        "booker_name": booking.guest_name,
        "guest_email": booking.guest_email,
        "booker_email": booking.guest_email,
        "guest_phone": booking.guest_phone,
        "booker_phone": booking.guest_phone,
        "guest_nationality": booking.guest_nationality,
        "booker_nationality": booking.guest_nationality,
        "total_amount_usd": total_amount,
        "total_price": total_amount,
        "currency": booking.currency,
        "status": booking.status,
        "stripe_payment_intent_id": booking.stripe_payment_intent_id,
        "stripe_session_id": booking.stripe_session_id,
        "paid_at": booking.paid_at.isoformat() if booking.paid_at else None,
        "cancelled_at": booking.cancelled_at.isoformat() if booking.cancelled_at else None,
        "cancellation_reason": booking.cancellation_reason,
        "created_at": booking.created_at.isoformat() if booking.created_at else None,
        "updated_at": booking.updated_at.isoformat() if booking.updated_at else None,
    }


def generate_booking_number() -> str:
    """Generate a unique booking number like MT-20260318-XXXX."""
    import random
    now = datetime.utcnow()
    date_str = now.strftime("%Y%m%d")
    rand_str = f"{random.randint(1, 9999):04d}"
    return f"MT-{date_str}-{rand_str}"
