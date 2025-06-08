from .base import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
import uuid
from app.core.constants.app import DEFAULT_TZ

class ConversationUser(Base):
    __tablename__ = "conversation_users"
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, server_default=func.timezone(DEFAULT_TZ, func.now()))
    updated_at = Column(DateTime, server_default=func.timezone(DEFAULT_TZ, func.now()), onupdate=func.timezone(DEFAULT_TZ, func.now()))