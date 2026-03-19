from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_db
from models.transport import TransportRoute, TransportTip
from utils.helpers import serialize_transport_route, serialize_transport_tip

router = APIRouter(prefix="/api/transport", tags=["Transport"])


@router.get("/routes")
async def list_transport_routes(
    lang: str = Query("en"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(TransportRoute).where(TransportRoute.is_active == True)

    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    routes = result.scalars().all()

    return {
        "items": [serialize_transport_route(r, lang) for r in routes],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/routes/{route_id}")
async def get_transport_route(
    route_id: str,
    lang: str = Query("en"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TransportRoute).where(TransportRoute.id == route_id))
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Transport route not found")

    return serialize_transport_route(route, lang)


@router.get("/tips")
async def list_transport_tips(
    lang: str = Query("en"),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(TransportTip).where(TransportTip.is_active == True)
    if category:
        query = query.where(TransportTip.category == category)
    query = query.order_by(TransportTip.display_order)

    result = await db.execute(query)
    tips = result.scalars().all()

    return {"items": [serialize_transport_tip(t, lang) for t in tips]}
