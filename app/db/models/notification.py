import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, Float, String

from app.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)

    category = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    processing_status = Column(String, default="pending")
