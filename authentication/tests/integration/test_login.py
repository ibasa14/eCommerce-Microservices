import httpx
import pytest
from src.constants import LOGIN_ROUTER_URL


@pytest.fixture
def api_authentication_url(api_url) -> str:
    return f"{api_url}{LOGIN_ROUTER_URL}"


@pytest.mark.asyncio
async def test_login(
    async_client: httpx.AsyncClient, api_authentication_url: str
) -> None:
    request = await async_client.post(
        api_authentication_url + "/login",
        data={"username": "test_user@ibc.com", "password": "test_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded", "accept": "application/json"},
    )
    request_json = request.json()

    assert request.status_code == 200
    assert request_json["authorized_account"]["name"] == "test_user"
    assert request_json["authorized_account"]["email"] == "test_user@ibc.com"
    assert request_json["authorized_account"]["is_active"] == True
    assert request_json["authorized_account"]["is_logged_in"] == False
    assert request_json["authorized_account"]["role_id"] == 2


