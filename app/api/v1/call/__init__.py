# app/api/v1/manage_chat/__init__.py

from fastapi import APIRouter
from app.api.v1.call.manage_call import router as manage_call_router

router = APIRouter(tags=["Call Management"])
router.include_router(manage_call_router)
