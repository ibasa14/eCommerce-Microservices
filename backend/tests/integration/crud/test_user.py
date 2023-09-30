import httpx


async def test_get_multiple_users(
    async_client: httpx.AsyncClient,
    api_url: str,
) -> None:
    response = await async_client.get(
        api_url + "/user",
    )
    assert [u["name"] for u in response.json()] == ["user1", "user2"]
