import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.sql import func


class ChatRoomUser(Base):
    __tablename__ = "chat_room_users"

    chat_room_id = Column(UUID(as_uuid=True), ForeignKey(
        "chat_rooms.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    joined_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)

    chat_room = relationship("ChatRoom", back_populates="users")
