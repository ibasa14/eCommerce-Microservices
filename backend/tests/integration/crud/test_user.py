from src.config.manager import settings
import httpx


async def test_get_multiple_users(async_client: httpx.AsyncClient) -> None:
    response = await async_client.get(
        f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}{settings.API_PREFIX}/user",
    )
    assert response.json() == [
        {"id": 1, "name": "user1"},
        {"id": 2, "name": "user2"},
    ]
