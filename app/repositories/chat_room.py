import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from app.models.user import User
from app.models.conversation import Conversation
from app.models.conversation_user import ConversationUser
from app.models.message import Message
from app.models.chat_room import ChatRoom
from app.models.chat_room_user import ChatRoomUser
from datetime import datetime

# ...existing conversation functions...


async def create_chat_room(session: AsyncSession, name: str, created_by: uuid.UUID, description: str = None, is_group: bool = True):
    chat_room = ChatRoom(
        name=name,
        created_by=created_by,
        description=description,
        is_group=is_group
    )
    session.add(chat_room)
    await session.flush()  # get chat_room.id
    # Add creator to the room
    session.add(ChatRoomUser(chat_room_id=chat_room.id, user_id=created_by))
    await session.commit()
    return chat_room


async def add_user_to_chat_room(session: AsyncSession, chat_room_id: uuid.UUID, user_id: uuid.UUID):
    exists = await session.execute(
        select(ChatRoomUser).where(
            ChatRoomUser.chat_room_id == chat_room_id,
            ChatRoomUser.user_id == user_id
        )
    )
    if exists.scalar_one_or_none():
        return False, "User already in chat room"
    session.add(ChatRoomUser(chat_room_id=chat_room_id, user_id=user_id))
    await session.commit()
    return True, None


async def remove_user_from_chat_room(session: AsyncSession, chat_room_id: uuid.UUID, user_id: uuid.UUID):
    await session.execute(
        delete(ChatRoomUser).where(
            ChatRoomUser.chat_room_id == chat_room_id,
            ChatRoomUser.user_id == user_id
        )
    )
    await session.commit()
    return True


async def get_users_in_chat_room(session: AsyncSession, chat_room_id: uuid.UUID):
    result = await session.execute(
        select(User).join(ChatRoomUser).where(
            ChatRoomUser.chat_room_id == chat_room_id)
    )
    return result.scalars().all()


async def send_chat_room_message(session: AsyncSession, chat_room_id: uuid.UUID, sender_id: uuid.UUID, content: str, message_type: str = "text"):
    msg = Message(
        chat_room_id=chat_room_id,
        sender_id=sender_id,
        content=content,
        message_type=message_type,
    )
    session.add(msg)
    await session.commit()
    await session.refresh(msg)
    return {
        "id": str(msg.id),
        "sender_id": str(msg.sender_id),
        "content": msg.content,
        "message_type": msg.message_type.value if hasattr(msg.message_type, "value") else str(msg.message_type),
        "seen": msg.seen,
        "sent_at": msg.sent_at.isoformat() if msg.sent_at else None,
        "created_at": msg.created_at.isoformat() if msg.created_at else None,
    }


async def get_messages_for_chat_room(session: AsyncSession, chat_room_id: uuid.UUID):
    result = await session.execute(
        select(Message).where(Message.chat_room_id ==
                              chat_room_id).order_by(Message.sent_at)
    )
    messages = result.scalars().all()
    return [
        {
            "id": str(msg.id),
            "sender_id": str(msg.sender_id),
            "content": msg.content,
            "message_type": msg.message_type.value if hasattr(msg.message_type, "value") else str(msg.message_type),
            "seen": msg.seen,
            "sent_at": msg.sent_at.isoformat() if msg.sent_at else None,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        }
        for msg in messages
    ]
