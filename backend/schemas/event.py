from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class EventCreate(BaseModel):
    slug: str
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
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    banner_image_url: Optional[str] = None
    is_active: Optional[bool] = True


class EventUpdate(BaseModel):
    slug: Optional[str] = None
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
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    banner_image_url: Optional[str] = None
    is_active: Optional[bool] = None


class EventLinkIds(BaseModel):
    restaurant_ids: Optional[List[str]] = None
    course_ids: Optional[List[str]] = None
    product_ids: Optional[List[str]] = None
    guide_ids: Optional[List[str]] = None
