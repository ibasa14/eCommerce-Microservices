import httpx
import pytest

from src.constants import USER_ROUTER_URL


@pytest.fixture
def api_user_url(api_url) -> str:
    return f"{api_url}{USER_ROUTER_URL}"


async def test_crud_users(
    async_client: httpx.AsyncClient, api_user_url: str
) -> None:
    response_get_multiple_users = await async_client.get(api_user_url)
    assert response_get_multiple_users.json() == [
        {"id": 1, "name": "user1"},
        {"id": 2, "name": "user2"},
    ]

    response_delete_user = await async_client.delete(
        api_user_url + "/1",
    )
    assert response_delete_user.status_code == 200

    response_after_deletion = await async_client.get(api_user_url)
    assert response_after_deletion.json() == [
        {"id": 2, "name": "user2"},
    ]
    response_create_user = await async_client.post(
        api_user_url,
        json={
            "name": "user3",
            "email": "email_user3@email.com",
            "password": "password",
            "role_id": 2,
        },
        headers={"Content-Type":"application/json"}
    )
    assert response_create_user.json() == {"id": 3, "name": "user3"}

    response_get_multiple_users_2 = await async_client.get(api_user_url)
    assert response_get_multiple_users_2.json() == [
        {"id": 2, "name": "user2"},
        {"id": 3, "name": "user3"},
    ]
    response_update_user = await async_client.put(
        api_user_url + "/3", json={"name": "user3_modified", "email":"email_user3@email.com_modified"}, headers={"Content-Type":"application/json"}
    )
    assert response_update_user.json() == {"id": 3, "name": "user3_modified"}
    response_get_user = await async_client.get(
        api_user_url + "/3",
    )
    assert response_get_user.json() == {"id": 3, "name": "user3_modified"}
