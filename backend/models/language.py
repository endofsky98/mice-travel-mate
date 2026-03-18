import uuid
from sqlalchemy import Column, String, Boolean, Integer, Text, ForeignKey
from database import Base


class Language(Base):
    __tablename__ = "languages"

    code = Column(String(10), primary_key=True)
    name_en = Column(String(100), nullable=False)
    name_native = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)


class UITranslation(Base):
    __tablename__ = "ui_translations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    language_code = Column(String(10), ForeignKey("languages.code", ondelete="CASCADE"), nullable=False, index=True)
    key = Column(String(255), nullable=False, index=True)
    value = Column(Text, nullable=False)
