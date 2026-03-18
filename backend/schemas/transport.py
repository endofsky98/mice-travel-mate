from pydantic import BaseModel
from typing import Optional, Any


class TransportRouteCreate(BaseModel):
    from_name_en: str
    from_name_ko: Optional[str] = None
    from_name_zh_cn: Optional[str] = None
    from_name_zh_tw: Optional[str] = None
    from_name_ja: Optional[str] = None
    from_name_es: Optional[str] = None
    to_name_en: str
    to_name_ko: Optional[str] = None
    to_name_zh_cn: Optional[str] = None
    to_name_zh_tw: Optional[str] = None
    to_name_ja: Optional[str] = None
    to_name_es: Optional[str] = None
    from_latitude: Optional[float] = None
    from_longitude: Optional[float] = None
    to_latitude: Optional[float] = None
    to_longitude: Optional[float] = None
    transport_modes: Optional[Any] = None
    route_polyline: Optional[str] = None
    is_active: Optional[bool] = True


class TransportRouteUpdate(BaseModel):
    from_name_en: Optional[str] = None
    from_name_ko: Optional[str] = None
    from_name_zh_cn: Optional[str] = None
    from_name_zh_tw: Optional[str] = None
    from_name_ja: Optional[str] = None
    from_name_es: Optional[str] = None
    to_name_en: Optional[str] = None
    to_name_ko: Optional[str] = None
    to_name_zh_cn: Optional[str] = None
    to_name_zh_tw: Optional[str] = None
    to_name_ja: Optional[str] = None
    to_name_es: Optional[str] = None
    from_latitude: Optional[float] = None
    from_longitude: Optional[float] = None
    to_latitude: Optional[float] = None
    to_longitude: Optional[float] = None
    transport_modes: Optional[Any] = None
    route_polyline: Optional[str] = None
    is_active: Optional[bool] = None


class TransportTipCreate(BaseModel):
    title_en: str
    title_ko: Optional[str] = None
    title_zh_cn: Optional[str] = None
    title_zh_tw: Optional[str] = None
    title_ja: Optional[str] = None
    title_es: Optional[str] = None
    content_en: Optional[str] = None
    content_ko: Optional[str] = None
    content_zh_cn: Optional[str] = None
    content_zh_tw: Optional[str] = None
    content_ja: Optional[str] = None
    content_es: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = 0
    is_active: Optional[bool] = True


class TransportTipUpdate(BaseModel):
    title_en: Optional[str] = None
    title_ko: Optional[str] = None
    title_zh_cn: Optional[str] = None
    title_zh_tw: Optional[str] = None
    title_ja: Optional[str] = None
    title_es: Optional[str] = None
    content_en: Optional[str] = None
    content_ko: Optional[str] = None
    content_zh_cn: Optional[str] = None
    content_zh_tw: Optional[str] = None
    content_ja: Optional[str] = None
    content_es: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
