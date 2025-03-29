from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    user_id: UUID
    title: str
    text: str


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    id: UUID
    created_at: datetime
    read_at: datetime | None
    category: str | None
    confidence: float | None
    processing_status: str

    model_config = ConfigDict(from_attributes=True)
