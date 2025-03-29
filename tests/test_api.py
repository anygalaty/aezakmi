import pytest


@pytest.mark.asyncio
async def test_create_notification(client):
    response = await client.post("/api/v1/notifications/", json={
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Test title",
        "text": "Warning: something went wrong"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test title"


@pytest.mark.asyncio
async def test_get_notification_list(client):
    response = await client.get("/api/v1/notifications")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_status_endpoint(client):
    create_resp = await client.post("/api/v1/notifications/", json={
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Status Test",
        "text": "some test text"
    })
    notif = create_resp.json()
    notif_id = notif["id"]

    status_response = await client.get(f"/api/v1/notifications/{notif_id}/status/")
    assert status_response.status_code == 200
    assert "status" in status_response.json()
