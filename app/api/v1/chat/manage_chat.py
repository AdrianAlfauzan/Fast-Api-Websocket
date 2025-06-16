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


@router.websocket("/ws/{channel_type}/{channel_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, channel_type: str, channel_id: str, user_id: str):
    """
    channel_type: 'conversation' or 'chat_room'
    channel_id: UUID of the conversation or chat room
    user_id: UUID of the user
    """
    ch_id = uuid.UUID(channel_id)
    usr_id = uuid.UUID(user_id)
    await manager.connect(channel_type, ch_id, websocket)
    try:
        async for session in get_async_session():
            while True:
                data = await websocket.receive_json()
                action = data.get("action", "send")

                if action == "send":
                    # Use correct field for conversation or chat_room
                    msg_kwargs = {
                        "sender_id": usr_id,
                        "content": data["content"],
                        "message_type": data.get("message_type", "text"),
                    }
                    if channel_type == "conversation":
                        msg_kwargs["conversation_id"] = ch_id
                    elif channel_type == "chat_room":
                        msg_kwargs["chat_room_id"] = ch_id

                    msg = Message(**msg_kwargs)
                    session.add(msg)
                    await session.commit()
                    await manager.broadcast(channel_type, ch_id, {
                        "action": "send",
                        "sender_id": str(usr_id),
                        "content": data["content"],
                        "message_type": data.get("message_type", "text"),
                        "message_id": str(msg.id),
                    })

                elif action == "update":
                    message_id = data.get("message_id")
                    new_content = data.get("content")
                    if not message_id or not new_content:
                        await websocket.send_json({"error": "Missing message_id or content for update"})
                        continue
                    message = await update_message(session, uuid.UUID(message_id), new_content)
                    if message:
                        await manager.broadcast(channel_type, ch_id, {
                            "action": "update",
                            "message_id": message_id,
                            "content": new_content,
                        })
                    else:
                        await websocket.send_json({"error": "Message not found"})

                elif action == "delete":
                    message_id = data.get("message_id")
                    if not message_id:
                        await websocket.send_json({"error": "Missing message_id for delete"})
                        continue
                    success = await delete_message(session, uuid.UUID(message_id))
                    if success:
                        await manager.broadcast(channel_type, ch_id, {
                            "action": "delete",
                            "message_id": message_id,
                        })
                    else:
                        await websocket.send_json({"error": "Message not found"})

                else:
                    await websocket.send_json({"error": "Unknown action"})
    except WebSocketDisconnect:
        manager.disconnect(channel_type, ch_id, websocket)
# @router.websocket("/ws/{conversation_id}/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, conversation_id: str, user_id: str):
#     conv_id = uuid.UUID(conversation_id)
#     usr_id = uuid.UUID(user_id)
#     await manager.connect(conv_id, websocket)
#     try:
#         async for session in get_async_session():
#             while True:
#                 data = await websocket.receive_json()
#                 # Default to "send" if not provided
#                 action = data.get("action", "send")

#                 if action == "send":
#                     msg = Message(
#                         conversation_id=conv_id,
#                         sender_id=usr_id,
#                         content=data["content"],
#                         message_type=data.get("message_type", "text"),
#                     )
#                     session.add(msg)
#                     await session.commit()
#                     await manager.broadcast(conv_id, {
#                         "action": "send",
#                         "sender_id": str(usr_id),
#                         "content": data["content"],
#                         "message_type": data.get("message_type", "text"),
#                         "message_id": str(msg.id),
#                     })

#                 elif action == "update":
#                     message_id = data.get("message_id")
#                     new_content = data.get("content")
#                     if not message_id or not new_content:
#                         await websocket.send_json({"error": "Missing message_id or content for update"})
#                         continue
#                     message = await update_message(session, uuid.UUID(message_id), new_content)
#                     if message:
#                         await manager.broadcast(conv_id, {
#                             "action": "update",
#                             "message_id": message_id,
#                             "content": new_content,
#                         })
#                     else:
#                         await websocket.send_json({"error": "Message not found"})

#                 elif action == "delete":
#                     message_id = data.get("message_id")
#                     if not message_id:
#                         await websocket.send_json({"error": "Missing message_id for delete"})
#                         continue
#                     success = await delete_message(session, uuid.UUID(message_id))
#                     if success:
#                         await manager.broadcast(conv_id, {
#                             "action": "delete",
#                             "message_id": message_id,
#                         })
#                     else:
#                         await websocket.send_json({"error": "Message not found"})

#                 else:
#                     await websocket.send_json({"error": "Unknown action"})
#     except WebSocketDisconnect:
#         manager.disconnect(conv_id, websocket)

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
async def list_messages(
    conversation_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    messages = await get_messages_for_conversation(session, uuid.UUID(conversation_id))
    return messages

