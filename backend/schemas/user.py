from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    nationality: Optional[str] = None
    preferred_language: Optional[str] = "en"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SocialLoginRequest(BaseModel):
    id_token: str
    name: Optional[str] = None
    authorization_code: Optional[str] = None  # for Apple


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    preferred_language: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    nationality: Optional[str] = None
    preferred_language: Optional[str] = "en"
    provider: str
    role: str
    is_admin: bool = False
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class BookmarkCreate(BaseModel):
    target_type: str  # restaurant, course, product, guide
    target_id: str


class BookmarkResponse(BaseModel):
    id: str
    user_id: str
    target_type: str
    target_id: str
    created_at: Optional[datetime] = None
