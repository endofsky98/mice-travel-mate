from pydantic import BaseModel
from typing import Optional


class LanguageCreate(BaseModel):
    code: str
    name_en: str
    name_native: str
    is_active: Optional[bool] = True
    display_order: Optional[int] = 0


class LanguageUpdate(BaseModel):
    name_en: Optional[str] = None
    name_native: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class UITranslationCreate(BaseModel):
    language_code: str
    key: str
    value: str


class UITranslationUpdate(BaseModel):
    value: str


class UITranslationBulkCreate(BaseModel):
    language_code: str
    translations: dict  # {"key": "value", ...}
