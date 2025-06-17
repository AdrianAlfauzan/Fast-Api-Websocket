# app/api/v1/manage_chat/__init__.py

from fastapi import APIRouter
from app.api.v1.chat.manage_chat import router as manage_chat_router
from app.api.v1.chat.manage_chat_rooms import router as manage_chat_room_router

router = APIRouter()
# Chat endpoints under /chat, tagged as "Chat Management"
router.include_router(
    manage_chat_router,
    prefix="/chat",
    tags=["Chat Management"]
)

# Chat room endpoints under /chat_room, tagged as "Chat Room Management"
router.include_router(
    manage_chat_room_router,
    prefix="/chat_room",
    tags=["Chat Room Management"]
)
