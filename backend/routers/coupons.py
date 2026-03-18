from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from pydantic import BaseModel

from database import get_db
from models.coupon import Coupon, CouponUsage
from models.user import User
from auth.dependencies import get_current_user_optional

router = APIRouter(prefix="/api/coupons", tags=["Coupons"])


class CouponValidateRequest(BaseModel):
    code: str
    order_amount_usd: Optional[float] = None
    product_id: Optional[str] = None
    category: Optional[str] = None


@router.post("/validate")
async def validate_coupon(
    data: CouponValidateRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """Validate a coupon code and return discount info."""
    # Look up the coupon
    result = await db.execute(
        select(Coupon).where(Coupon.code == data.code)
    )
    coupon = result.scalar_one_or_none()

    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon code")

    if not coupon.is_active:
        raise HTTPException(status_code=400, detail="This coupon is no longer active")

    # Check date validity
    today = date.today()
    if coupon.start_date and today < coupon.start_date:
        raise HTTPException(status_code=400, detail="This coupon is not yet valid")
    if coupon.end_date and today > coupon.end_date:
        raise HTTPException(status_code=400, detail="This coupon has expired")

    # Check total usage limit
    if coupon.total_limit is not None and coupon.used_count >= coupon.total_limit:
        raise HTTPException(status_code=400, detail="This coupon has reached its usage limit")

    # Check per-user limit
    if current_user and coupon.per_user_limit:
        user_usage_result = await db.execute(
            select(func.count(CouponUsage.id)).where(
                CouponUsage.coupon_id == coupon.id,
                CouponUsage.user_id == current_user.id,
            )
        )
        user_usage_count = user_usage_result.scalar() or 0
        if user_usage_count >= coupon.per_user_limit:
            raise HTTPException(status_code=400, detail="You have already used this coupon")

    # Check minimum order amount
    if coupon.min_order_usd and data.order_amount_usd:
        if data.order_amount_usd < float(coupon.min_order_usd):
            raise HTTPException(
                status_code=400,
                detail=f"Minimum order amount is ${float(coupon.min_order_usd):.2f}",
            )

    # Check applicable scope
    if coupon.applicable_to == "product" and coupon.applicable_ids:
        if data.product_id and data.product_id not in coupon.applicable_ids:
            raise HTTPException(status_code=400, detail="This coupon is not applicable to this product")

    if coupon.applicable_to == "category" and coupon.applicable_categories:
        if data.category and data.category not in coupon.applicable_categories:
            raise HTTPException(status_code=400, detail="This coupon is not applicable to this category")

    # Calculate discount
    discount_amount = 0.0
    if coupon.discount_type == "fixed":
        discount_amount = float(coupon.discount_value)
    elif coupon.discount_type == "percentage":
        if data.order_amount_usd:
            discount_amount = data.order_amount_usd * float(coupon.discount_value) / 100
            if coupon.max_discount_usd:
                discount_amount = min(discount_amount, float(coupon.max_discount_usd))
        else:
            discount_amount = 0.0  # Cannot calculate without order amount

    return {
        "valid": True,
        "coupon": {
            "id": coupon.id,
            "code": coupon.code,
            "name": coupon.name,
            "description": coupon.description,
            "discount_type": coupon.discount_type,
            "discount_value": float(coupon.discount_value),
            "max_discount_usd": float(coupon.max_discount_usd) if coupon.max_discount_usd else None,
            "min_order_usd": float(coupon.min_order_usd) if coupon.min_order_usd else None,
            "applicable_to": coupon.applicable_to,
            "start_date": str(coupon.start_date) if coupon.start_date else None,
            "end_date": str(coupon.end_date) if coupon.end_date else None,
        },
        "calculated_discount_usd": round(discount_amount, 2),
    }
