import json
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client
from app.db.session import get_db
from app.schemas.notification import NotificationCreate, NotificationRead
from app.services.notification_service import (
    create_notification,
    get_notification,
    get_notifications,
    mark_as_read,
)

router = APIRouter()
CACHE_KEY = "notifications_list"
CACHE_TTL = 60


@router.post("/", response_model=NotificationRead)
async def create(data: NotificationCreate, db: AsyncSession = Depends(get_db)):
    return await create_notification(db, data)


@router.get("/", response_model=list[NotificationRead])
async def list_all(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    if skip == 0 and limit == 10:
        cached = await redis_client.get(CACHE_KEY)
        if cached:
            return json.loads(cached)

    notifs = await get_notifications(db, skip, limit)

    if skip == 0 and limit == 10:
        await redis_client.set(
            CACHE_KEY,
            json.dumps([n.__dict__ for n in notifs], default=str),
            ex=CACHE_TTL
        )

    return notifs


@router.get("/{notification_id}", response_model=NotificationRead)
async def get_one(notification_id: UUID, db: AsyncSession = Depends(get_db)):
    notif = await get_notification(db, notification_id)
    return notif


@router.post("/{notification_id}/read", response_model=NotificationRead)
async def mark_read(notification_id: UUID, db: AsyncSession = Depends(get_db)):
    notif = await mark_as_read(db, notification_id)
    return notif


@router.get("/{notification_id}/status")
async def get_status(notification_id: UUID, db: AsyncSession = Depends(get_db)):
    notif = await get_notification(db, notification_id)
    return {"status": notif.processing_status}
