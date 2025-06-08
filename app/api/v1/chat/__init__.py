# app/api/v1/manage_chat/__init__.py

from fastapi import APIRouter
from app.api.v1.chat.manage_chat import router as manage_chat_router

router = APIRouter(tags=["Chat Management"])
router.include_router(manage_chat_router)
