from .base import Base

from sqlalchemy import UUID,  Column,  DateTime, func
import uuid
from app.core.constants.app import DEFAULT_TZ

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=func.timezone(DEFAULT_TZ, func.now()))
