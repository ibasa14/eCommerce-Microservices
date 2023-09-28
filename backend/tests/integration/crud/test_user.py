# import pytest
# import httpx
from src.config.manager import settings
from fastapi.testclient import TestClient


def test_get_multiple_users(sync_client: TestClient) -> None:
    url = "http://localhost:8000/api/user"
    # response = await async_client.get(
    #         f"http://{settings.SERVER_PORT}:{settings.SERVER_PORT}/{settings.API_PREFIX}/user",
    #     )
    # response2 = await async_client.get(url)
    response = sync_client.get(url)
    assert response.json() == ""
