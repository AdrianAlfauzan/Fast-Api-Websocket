from pydantic import BaseModel
from typing import Optional


class ChatRoomCreate(BaseModel):
    name: str
    created_by: str  # UUID as string
    description: Optional[str] = None
    is_group: Optional[bool] = True


class ChatRoomResponse(BaseModel):
    chat_room_id: str
    name: str
    description: Optional[str] = None
    is_group: bool
    created_by: str
    created_at: Optional[str] = None
