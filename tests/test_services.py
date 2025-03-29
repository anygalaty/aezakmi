from uuid import UUID

import pytest

from app.db.models.notification import Notification
from app.schemas.notification import NotificationCreate
from app.services.notification_service import create_notification


@pytest.mark.asyncio
async def test_create_notification_service(db_session):
    data = NotificationCreate(
        user_id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        title="Service test",
        text="This is a test"
    )
    notif = await create_notification(db_session, data)
    assert isinstance(notif, Notification)
    assert notif.title == "Service test"
