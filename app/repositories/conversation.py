import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from app.models.user import User
from app.models.conversation import Conversation
from app.models.conversation_user import ConversationUser  
from app.models.message import Message
from datetime import datetime
async def create_conversation_by_username(
    session: AsyncSession,
    current_user_id: uuid.UUID,
    target_username: str
):
    # 1. Find the target user by username
    result = await session.execute(select(User).where(User.username == target_username))
    target_user = result.scalar_one_or_none()
    if not target_user:
        return None, "User not found"

    # 2. Create a new conversation
    conversation = Conversation()
    session.add(conversation)
    await session.flush()  # To get conversation.id

    # 3. Add both users to conversation_users table
    await session.execute(
        insert(conversation.__table__.metadata.tables['conversation_users']).values([
            {"conversation_id": conversation.id, "user_id": current_user_id},
            {"conversation_id": conversation.id, "user_id": target_user.id},
        ])
    )
    await session.commit()
    return conversation, None


async def get_conversations_for_user(session, user_id):

    result = await session.execute(
        select(Conversation).join(ConversationUser).where(ConversationUser.user_id == user_id)
    )
    conversations = result.scalars().all()

    chat_list = []
    for conv in conversations:
        other_user_result = await session.execute(
            select(User)
            .join(ConversationUser, User.id == ConversationUser.user_id)
            .where(
                ConversationUser.conversation_id == conv.id,
                ConversationUser.user_id != user_id
            )
        )
        other_user = other_user_result.scalar_one_or_none()
        chat_list.append({
            "conversation_id": str(conv.id),
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "user": {
                "id": str(other_user.id) if other_user else None,
                "username": other_user.username if other_user else None,
                "full_name": other_user.full_name if other_user else None,
            }
        })
    return chat_list


async def get_messages_for_conversation(session, conversation_id):
    result = await session.execute(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.sent_at)
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


async def send_message(session, conversation_id, sender_id, content, message_type):
    msg = Message(
        conversation_id=conversation_id,
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

async def update_message(session, message_id, content):
    msg = await session.get(Message, message_id)
    if not msg:
        return None
    msg.content = content
    msg.updated_at = datetime.utcnow()
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
        "updated_at": msg.updated_at.isoformat() if msg.updated_at else None,
    }

async def delete_message(session, message_id):
    msg = await session.get(Message, message_id)
    if not msg:
        return False
    await session.delete(msg)
    await session.commit()
    return True