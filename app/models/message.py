
from .base import Base

from sqlalchemy import Column, DateTime, Boolean, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
import enum
class MessageType(str, enum.Enum):
    text = "text"
    image = "image"
    video = "video"
    file = "file"

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType, name="message_type_enum"))
    seen = Column(Boolean, default=False)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)