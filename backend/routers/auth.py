import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User
from schemas.user import (
    UserRegister,
    UserLogin,
    SocialLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserUpdate,
    UserResponse,
    TokenResponse,
)
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from auth.dependencies import get_current_user
from auth.social import verify_google_token, verify_apple_token
from utils.email import send_password_reset_email

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        nationality=user.nationality,
        preferred_language=user.preferred_language,
        provider=user.provider,
        role=user.role,
        is_admin=user.role in ("admin", "superadmin"),
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def create_token_response(user: User) -> dict:
    access_token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user_to_response(user),
    }


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if email exists
    result = await db.execute(select(User).where(User.email == data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")

    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 최소 8자 이상이어야 합니다")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
        nationality=data.nationality,
        preferred_language=data.preferred_language or "en",
        provider="local",
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return create_token_response(user)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다")

    if not user.password_hash:
        raise HTTPException(status_code=401, detail="This account uses social login. Please sign in with Google or Apple.")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    return create_token_response(user)


@router.post("/social/google", response_model=TokenResponse)
async def google_login(data: SocialLoginRequest, db: AsyncSession = Depends(get_db)):
    google_user = await verify_google_token(data.id_token)
    if not google_user:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = google_user["email"]
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        # Update provider info if needed
        if user.provider == "local":
            user.provider = "google"
            user.provider_id = google_user["sub"]
    else:
        user = User(
            email=email,
            name=data.name or google_user.get("name", email.split("@")[0]),
            provider="google",
            provider_id=google_user["sub"],
        )
        db.add(user)

    await db.flush()
    await db.refresh(user)

    return create_token_response(user)


@router.post("/social/apple", response_model=TokenResponse)
async def apple_login(data: SocialLoginRequest, db: AsyncSession = Depends(get_db)):
    apple_user = await verify_apple_token(
        authorization_code=data.authorization_code or "",
        id_token=data.id_token,
    )
    if not apple_user:
        raise HTTPException(status_code=401, detail="Invalid Apple token")

    email = apple_user["email"]
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        if user.provider == "local":
            user.provider = "apple"
            user.provider_id = apple_user["sub"]
    else:
        user = User(
            email=email,
            name=data.name or apple_user.get("name", email.split("@")[0]),
            provider="apple",
            provider_id=apple_user["sub"],
        )
        db.add(user)

    await db.flush()
    await db.refresh(user)

    return create_token_response(user)


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    if user and user.provider == "local":
        token = create_password_reset_token(user.email)
        await send_password_reset_email(user.email, token)

    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    email = verify_password_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if len(data.new_password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 최소 8자 이상이어야 합니다")

    user.password_hash = hash_password(data.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    await db.flush()

    return {"message": "Password has been reset successfully"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return user_to_response(current_user)


@router.put("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.name is not None:
        current_user.name = data.name
    if data.nationality is not None:
        current_user.nationality = data.nationality
    if data.preferred_language is not None:
        current_user.preferred_language = data.preferred_language

    await db.flush()
    await db.refresh(current_user)

    return user_to_response(current_user)


@router.delete("/me")
async def delete_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_user.is_active = False
    await db.flush()
    return {"message": "Account deactivated successfully"}
