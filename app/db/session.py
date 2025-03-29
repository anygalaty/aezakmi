from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

sync_engine = create_engine(settings.DATABASE_URL_SYNC, echo=False)
SyncSessionLocal = sessionmaker(bind=sync_engine)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
