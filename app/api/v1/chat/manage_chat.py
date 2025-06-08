from app.repositories.conversation import create_conversation_by_username
from app.repositories.conversation import get_conversations_for_user
from app.core.database import get_session
import uuid
from fastapi import APIRouter, HTTPException
from app.repositories.conversation import (
    create_conversation_by_username,
    get_conversations_for_user,
    get_messages_for_conversation,
    send_message,
    update_message,
    delete_message,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket, WebSocketDisconnect
from app.core.connection_manager import ConnectionManager
from app.schemas.chat_mgt import ChatMessage
from app.schemas.chat_mgt import ChatMessage, ChatMessageCreate, ChatMessageUpdate
from app.models.message import Message
from app.core.database import get_async_session
from fastapi import Depends
router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/{conversation_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str, user_id: str):
    conv_id = uuid.UUID(conversation_id)
    usr_id = uuid.UUID(user_id)
    await manager.connect(conv_id, websocket)
    try:
        async for session in get_async_session():
            while True:
                data = await websocket.receive_json()
                msg = Message(
                    conversation_id=conv_id,
                    sender_id=usr_id,
                    content=data["content"],
                    message_type=data.get("message_type", "text"),
                )
                session.add(msg)
                await session.commit()
                # Broadcast to all in conversation
                await manager.broadcast(conv_id, {
                    "sender_id": str(usr_id),
                    "content": data["content"],
                    "message_type": data.get("message_type", "text"),
                })
    except WebSocketDisconnect:
        manager.disconnect(conv_id, websocket)


@router.post("/conversations/add_by_username")
async def add_user_to_conversation(
    current_user_id: str,
    target_username: str,
    session: AsyncSession = Depends(get_async_session)
):
    conversation, error = await create_conversation_by_username(
        session, uuid.UUID(current_user_id), target_username
    )
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"conversation_id": str(conversation.id)}


@router.get("/conversations/list")
async def list_conversations(
    current_user_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    chat_list = await get_conversations_for_user(session, uuid.UUID(current_user_id))
    return chat_list
    
@router.get("/conversations/{conversation_id}/messages", response_model=list[ChatMessage])
async def list_messages(conversation_id: str):
    async with get_session() as session:
        messages = await get_messages_for_conversation(session, uuid.UUID(conversation_id))
        return messages


# chat message endpoints 
@router.put("/messages/{message_id}", response_model=ChatMessage)
async def update_message_endpoint(message_id: str, body: ChatMessageUpdate):
    async with get_session() as session:
        message = await update_message(
            session,
            uuid.UUID(message_id),
            body.content,
        )
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return message


@router.delete("/messages/{message_id}")
async def delete_message_endpoint(message_id: str):
    async with get_session() as session:
        success = await delete_message(session, uuid.UUID(message_id))
        if not success:
            raise HTTPException(status_code=404, detail="Message not found")
        return {"detail": "Message deleted"}
