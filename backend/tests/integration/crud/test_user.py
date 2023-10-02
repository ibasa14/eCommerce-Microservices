import httpx


async def test_get_multiple_users(
    async_client: httpx.AsyncClient, api_url: str
) -> None:
    response = await async_client.get(
        api_url + "/user",
    )
    assert response.json() == [
        {"id": 1, "name": "user1"},
        {"id": 2, "name": "user2"},
    ]
