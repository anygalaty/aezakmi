import asyncio
from uuid import UUID

from celery import shared_task
from sqlalchemy.orm import Session

from app.db.models.notification import Notification
from app.db.session import SyncSessionLocal
from app.services.ai_analyzer import analyze_text


@shared_task
def process_notification(notification_id: str, text: str):
    db: Session = SyncSessionLocal()

    try:
        notif = db.query(Notification).filter(Notification.id == UUID(notification_id)).first()
        if not notif:
            return

        notif.processing_status = "processing"
        db.commit()

        result = asyncio.run(analyze_text(text))

        notif.category = result["category"]
        notif.confidence = result["confidence"]
        notif.processing_status = "completed"
        db.commit()

    except Exception as e:
        if notif:
            notif.processing_status = "failed"
            db.commit()
        raise e

    finally:
        db.close()
