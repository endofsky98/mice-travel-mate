from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.language import Language, UITranslation

router = APIRouter(prefix="/api/languages", tags=["Languages"])


@router.get("/")
async def list_languages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Language).where(Language.is_active == True).order_by(Language.display_order)
    )
    languages = result.scalars().all()

    return {
        "items": [
            {
                "code": lang.code,
                "name_en": lang.name_en,
                "name_native": lang.name_native,
                "is_active": lang.is_active,
                "display_order": lang.display_order,
            }
            for lang in languages
        ]
    }


@router.get("/{code}/translations")
async def get_translations(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    # Verify language exists
    lang_result = await db.execute(select(Language).where(Language.code == code))
    language = lang_result.scalar_one_or_none()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    result = await db.execute(
        select(UITranslation).where(UITranslation.language_code == code)
    )
    translations = result.scalars().all()

    # Return as key-value dict
    translation_dict = {}
    for t in translations:
        translation_dict[t.key] = t.value

    return {
        "language_code": code,
        "translations": translation_dict,
    }
