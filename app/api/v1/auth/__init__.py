# app/api/v1/employee_mgt/__init__.py

from fastapi import APIRouter
from app.api.v1.auth.manage_auth import router as manage_auth_router

router = APIRouter(tags=["Auth Management"])
router.include_router(manage_auth_router)
