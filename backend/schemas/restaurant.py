from pydantic import BaseModel
from typing import Optional, List, Any


class RestaurantCreate(BaseModel):
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
    category: Optional[str] = None
    price_range: Optional[int] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    opening_hours: Optional[Any] = None
    menu_highlights: Optional[Any] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = True


class RestaurantUpdate(BaseModel):
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
    category: Optional[str] = None
    price_range: Optional[int] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    opening_hours: Optional[Any] = None
    menu_highlights: Optional[Any] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = None
