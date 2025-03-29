from datetime import datetime
from uuid import UUID

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.redis import redis_client
from app.db.models.notification import Notification
from app.schemas.notification import NotificationCreate
from app.tasks import process_notification


async def create_notification(db: AsyncSession, data: NotificationCreate) -> Notification:
    notif = Notification(**data.model_dump())
    db.add(notif)
    await db.commit()
    await db.refresh(notif)

    process_notification.delay(str(notif.id), notif.text)
    await redis_client.delete("notifications_list")

    return notif


async def get_notification(db: AsyncSession, notification_id: UUID) -> Notification | None:
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    return result.scalar_one_or_none()


async def get_notifications(db: AsyncSession, skip: int = 0, limit: int = 10) -> Sequence[Notification]:
    result = await db.execute(
        select(Notification).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def mark_as_read(db: AsyncSession, notification_id: UUID) -> Notification | None:
    notif = await get_notification(db, notification_id)
    if notif:
        notif.read_at = datetime.now()
        await db.commit()
        await db.refresh(notif)
    return notif
