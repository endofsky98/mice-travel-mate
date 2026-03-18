import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional
from pydantic import BaseModel, Field

from database import get_db
from models.chat import ChatRoom, ChatMessage
from models.guide import Guide
from models.user import User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatRoomCreate(BaseModel):
    guide_id: str


class MessageCreate(BaseModel):
    message_type: str = Field("text", pattern="^(text|image)$")
    content: Optional[str] = None
    image_url: Optional[str] = None


@router.get("/rooms")
async def list_chat_rooms(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's chat rooms."""
    query = select(ChatRoom).where(
        ChatRoom.user_id == current_user.id,
        ChatRoom.is_active == True,
    )

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(ChatRoom.last_message_at.desc().nullslast()).offset(offset).limit(per_page)
    result = await db.execute(query)
    rooms = result.scalars().all()

    # Fetch guide info for each room
    guide_ids = list({r.guide_id for r in rooms})
    guides_map = {}
    if guide_ids:
        guides_result = await db.execute(select(Guide).where(Guide.id.in_(guide_ids)))
        for g in guides_result.scalars().all():
            guides_map[g.id] = g

    return {
        "items": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "guide_id": r.guide_id,
                "guide_name": guides_map.get(r.guide_id, None) and guides_map[r.guide_id].name_en,
                "guide_profile_image": guides_map.get(r.guide_id, None) and guides_map[r.guide_id].profile_image_url,
                "last_message": r.last_message,
                "last_message_at": r.last_message_at.isoformat() if r.last_message_at else None,
                "user_unread_count": r.user_unread_count,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rooms
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.post("/rooms")
async def create_chat_room(
    data: ChatRoomCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a chat room with a guide. Returns existing room if already exists."""
    # Check guide exists
    guide_result = await db.execute(select(Guide).where(Guide.id == data.guide_id))
    guide = guide_result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    # Check for existing room
    existing = await db.execute(
        select(ChatRoom).where(
            ChatRoom.user_id == current_user.id,
            ChatRoom.guide_id == data.guide_id,
            ChatRoom.is_active == True,
        )
    )
    room = existing.scalar_one_or_none()
    if room:
        return {
            "id": room.id,
            "user_id": room.user_id,
            "guide_id": room.guide_id,
            "guide_name": guide.name_en,
            "guide_profile_image": guide.profile_image_url,
            "last_message": room.last_message,
            "last_message_at": room.last_message_at.isoformat() if room.last_message_at else None,
            "user_unread_count": room.user_unread_count,
            "created_at": room.created_at.isoformat() if room.created_at else None,
            "is_new": False,
        }

    # Create new room
    room = ChatRoom(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        guide_id=data.guide_id,
    )
    db.add(room)
    await db.flush()
    await db.refresh(room)

    return {
        "id": room.id,
        "user_id": room.user_id,
        "guide_id": room.guide_id,
        "guide_name": guide.name_en,
        "guide_profile_image": guide.profile_image_url,
        "last_message": room.last_message,
        "last_message_at": None,
        "user_unread_count": 0,
        "created_at": room.created_at.isoformat() if room.created_at else None,
        "is_new": True,
    }


@router.get("/rooms/{room_id}/messages")
async def list_messages(
    room_id: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List messages in a chat room."""
    # Verify room access
    room_result = await db.execute(
        select(ChatRoom).where(
            ChatRoom.id == room_id,
            ChatRoom.user_id == current_user.id,
        )
    )
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    query = select(ChatMessage).where(ChatMessage.room_id == room_id)

    # Count
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Paginate (newest first)
    offset = (page - 1) * per_page
    query = query.order_by(ChatMessage.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    messages = result.scalars().all()

    return {
        "items": [
            {
                "id": m.id,
                "room_id": m.room_id,
                "sender_type": m.sender_type,
                "sender_id": m.sender_id,
                "message_type": m.message_type,
                "content": m.content,
                "image_url": m.image_url,
                "is_read": m.is_read,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.post("/rooms/{room_id}/messages")
async def send_message(
    room_id: str,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message in a chat room."""
    # Verify room access
    room_result = await db.execute(
        select(ChatRoom).where(
            ChatRoom.id == room_id,
            ChatRoom.user_id == current_user.id,
        )
    )
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    if data.message_type == "text" and not data.content:
        raise HTTPException(status_code=400, detail="Text message must have content")
    if data.message_type == "image" and not data.image_url:
        raise HTTPException(status_code=400, detail="Image message must have image_url")

    message = ChatMessage(
        id=str(uuid.uuid4()),
        room_id=room_id,
        sender_type="user",
        sender_id=current_user.id,
        message_type=data.message_type,
        content=data.content,
        image_url=data.image_url,
    )
    db.add(message)

    # Update room metadata
    now = datetime.utcnow()
    room.last_message = data.content or "[Image]"
    room.last_message_at = now
    room.guide_unread_count = (room.guide_unread_count or 0) + 1
    room.updated_at = now

    await db.flush()
    await db.refresh(message)

    return {
        "id": message.id,
        "room_id": message.room_id,
        "sender_type": message.sender_type,
        "sender_id": message.sender_id,
        "message_type": message.message_type,
        "content": message.content,
        "image_url": message.image_url,
        "is_read": message.is_read,
        "created_at": message.created_at.isoformat() if message.created_at else None,
    }


@router.put("/messages/{message_id}/read")
async def mark_message_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a message as read."""
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.id == message_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Verify the user has access to this room
    room_result = await db.execute(
        select(ChatRoom).where(
            ChatRoom.id == message.room_id,
            ChatRoom.user_id == current_user.id,
        )
    )
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=403, detail="Access denied")

    message.is_read = True
    await db.flush()

    # Decrease unread count for user
    if room.user_unread_count and room.user_unread_count > 0:
        room.user_unread_count -= 1
        await db.flush()

    return {"message": "Message marked as read"}
