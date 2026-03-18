from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date


class GuideCreate(BaseModel):
    name_en: str
    name_ko: Optional[str] = None
    name_zh_cn: Optional[str] = None
    name_zh_tw: Optional[str] = None
    name_ja: Optional[str] = None
    name_es: Optional[str] = None
    bio_en: Optional[str] = None
    bio_ko: Optional[str] = None
    bio_zh_cn: Optional[str] = None
    bio_zh_tw: Optional[str] = None
    bio_ja: Optional[str] = None
    bio_es: Optional[str] = None
    profile_image_url: Optional[str] = None
    languages: Optional[List[Any]] = None
    specialties: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    price_per_hour_usd: Optional[float] = None
    price_half_day_usd: Optional[float] = None
    price_full_day_usd: Optional[float] = None
    services_en: Optional[str] = None
    services_ko: Optional[str] = None
    services_zh_cn: Optional[str] = None
    services_zh_tw: Optional[str] = None
    services_ja: Optional[str] = None
    services_es: Optional[str] = None
    status: Optional[str] = "active"


class GuideUpdate(BaseModel):
    name_en: Optional[str] = None
    name_ko: Optional[str] = None
    name_zh_cn: Optional[str] = None
    name_zh_tw: Optional[str] = None
    name_ja: Optional[str] = None
    name_es: Optional[str] = None
    bio_en: Optional[str] = None
    bio_ko: Optional[str] = None
    bio_zh_cn: Optional[str] = None
    bio_zh_tw: Optional[str] = None
    bio_ja: Optional[str] = None
    bio_es: Optional[str] = None
    profile_image_url: Optional[str] = None
    languages: Optional[List[Any]] = None
    specialties: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    price_per_hour_usd: Optional[float] = None
    price_half_day_usd: Optional[float] = None
    price_full_day_usd: Optional[float] = None
    services_en: Optional[str] = None
    services_ko: Optional[str] = None
    services_zh_cn: Optional[str] = None
    services_zh_tw: Optional[str] = None
    services_ja: Optional[str] = None
    services_es: Optional[str] = None
    status: Optional[str] = None


class GuideAvailabilityUpdate(BaseModel):
    date: date
    is_available: bool
