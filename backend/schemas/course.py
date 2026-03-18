from pydantic import BaseModel
from typing import Optional, List


class CourseSpotCreate(BaseModel):
    spot_order: int = 0
    name_en: str
    name_ko: Optional[str] = None
    name_zh_cn: Optional[str] = None
    name_zh_tw: Optional[str] = None
    name_ja: Optional[str] = None
    name_es: Optional[str] = None
    description_en: Optional[str] = None
    description_ko: Optional[str] = None
    description_zh_cn: Optional[str] = None
    description_zh_tw: Optional[str] = None
    description_ja: Optional[str] = None
    description_es: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    stay_duration_minutes: Optional[int] = None
    image_url: Optional[str] = None
    restaurant_id: Optional[str] = None


class CourseSpotTransitionCreate(BaseModel):
    from_spot_id: str
    to_spot_id: str
    transport_mode: Optional[str] = None
    duration_minutes: Optional[int] = None
    distance_km: Optional[float] = None
    route_polyline: Optional[str] = None


class CourseCreate(BaseModel):
    name_en: str
    name_ko: Optional[str] = None
    name_zh_cn: Optional[str] = None
    name_zh_tw: Optional[str] = None
    name_ja: Optional[str] = None
    name_es: Optional[str] = None
    description_en: Optional[str] = None
    description_ko: Optional[str] = None
    description_zh_cn: Optional[str] = None
    description_zh_tw: Optional[str] = None
    description_ja: Optional[str] = None
    description_es: Optional[str] = None
    duration_type: Optional[str] = None
    theme: Optional[str] = None
    region: Optional[str] = None
    difficulty: Optional[str] = None
    total_duration_minutes: Optional[int] = None
    total_distance_km: Optional[float] = None
    estimated_transport_cost: Optional[float] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True


class CourseUpdate(BaseModel):
    name_en: Optional[str] = None
    name_ko: Optional[str] = None
    name_zh_cn: Optional[str] = None
    name_zh_tw: Optional[str] = None
    name_ja: Optional[str] = None
    name_es: Optional[str] = None
    description_en: Optional[str] = None
    description_ko: Optional[str] = None
    description_zh_cn: Optional[str] = None
    description_zh_tw: Optional[str] = None
    description_ja: Optional[str] = None
    description_es: Optional[str] = None
    duration_type: Optional[str] = None
    theme: Optional[str] = None
    region: Optional[str] = None
    difficulty: Optional[str] = None
    total_duration_minutes: Optional[int] = None
    total_distance_km: Optional[float] = None
    estimated_transport_cost: Optional[float] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
