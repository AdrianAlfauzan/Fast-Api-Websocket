from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    id: str
    sender_id: str
    content: str
    message_type: str
    seen: bool
    sent_at: Optional[str]
    created_at: Optional[str]

class ChatMessageCreate(BaseModel):
    sender_id: str
    content: str
    message_type: str


class ChatMessageUpdate(BaseModel):
    content: str
