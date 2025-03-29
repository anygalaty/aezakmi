import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app import tasks
from app.db.session import AsyncSessionLocal
from app.main import app


@pytest.fixture(autouse=True)
def mock_celery(monkeypatch):
    monkeypatch.setattr(tasks.process_notification, "delay", lambda *args, **kwargs: None)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url="http://test",
            follow_redirects=True
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()
