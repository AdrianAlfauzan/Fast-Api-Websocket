from app.repositories.chat_room import (
    create_chat_room,
    add_user_to_chat_room,
    get_users_in_chat_room,
    get_messages_for_chat_room,
    send_chat_room_message,
)
from app.schemas.chat_mgt import ChatMessage
from app.schemas.chat_room_mgt import ChatRoomCreate, ChatRoomResponse

import uuid
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.connection_manager import ConnectionManager
from app.core.database import get_async_session
from fastapi import Depends
router = APIRouter()
manager = ConnectionManager()


@router.post("/chat_rooms/create", response_model=ChatRoomResponse)
async def create_room(
    chat_room: ChatRoomCreate,
    session: AsyncSession = Depends(get_async_session)
):
    room = await create_chat_room(
        session,
        chat_room.name,
        uuid.UUID(chat_room.created_by),
        chat_room.description
    )
    return ChatRoomResponse(
        chat_room_id=str(room.id),
        name=room.name,
        description=room.description,
        is_group=room.is_group,
        created_by=str(room.created_by),
        created_at=room.created_at
    )

async def create_room(
    name: str,
    created_by: str,
    description: str = None,
    session: AsyncSession = Depends(get_async_session)
):
    room = await create_chat_room(session, name, uuid.UUID(created_by), description)
    return {"chat_room_id": str(room.id)}


@router.post("/chat_rooms/{chat_room_id}/add_user")
async def add_user(
    chat_room_id: str,
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    success, error = await add_user_to_chat_room(session, uuid.UUID(chat_room_id), uuid.UUID(user_id))
    if not success:
        raise HTTPException(status_code=400, detail=error)
    return {"status": "user added"}


@router.get("/chat_rooms/{chat_room_id}/users")
async def list_users(
    chat_room_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    users = await get_users_in_chat_room(session, uuid.UUID(chat_room_id))
    return [
        {
            "id": str(user.id),
            "username": user.username,
            "full_name": getattr(user, "full_name", None),
        }
        for user in users
    ]


@router.get("/chat_rooms/{chat_room_id}/messages", response_model=list[ChatMessage])
async def list_chat_room_messages(
    chat_room_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    messages = await get_messages_for_chat_room(session, uuid.UUID(chat_room_id))
    return messages


@router.post("/chat_rooms/{chat_room_id}/send_message", response_model=ChatMessage)
async def send_room_message(
    chat_room_id: str,
    sender_id: str,
    content: str,
    message_type: str = "text",
    session: AsyncSession = Depends(get_async_session)
):
    msg = await send_chat_room_message(
        session,
        uuid.UUID(chat_room_id),
        uuid.UUID(sender_id),
        content,
        message_type,
    )
    return msg
