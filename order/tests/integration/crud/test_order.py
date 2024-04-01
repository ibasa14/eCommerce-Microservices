from unittest import mock
from unittest.mock import AsyncMock

import httpx
import pytest
from src.constants import ORDER_ROUTER_URL


@pytest.fixture
def api_order_url(api_url) -> str:
    return f"{api_url}{ORDER_ROUTER_URL}"


@pytest.mark.asyncio
async def test_crud_orders_non_authenticated(
    async_non_authenticated_client: httpx.AsyncClient,
    api_order_url: str,
) -> None:
    response_get_multiple_order_for_user = (
        await async_non_authenticated_client.get(api_order_url)
    )
    assert response_get_multiple_order_for_user.status_code == 401

    response_get_order = await async_non_authenticated_client.get(
        api_order_url + "/1",
    )
    assert response_get_order.status_code == 401

    response_create_order = await async_non_authenticated_client.post(
        api_order_url,
        json={
            "total_price": 923.1223,
        },
        headers={"Content-Type": "application/json"},
    )
    assert response_create_order.status_code == 401

    response_delete_order = await async_non_authenticated_client.delete(
        api_order_url + "/1",
    )
    assert response_delete_order.status_code == 401


@mock.patch(
    "src.crud.order.OrderCRUD._is_product_updated",
    return_value=AsyncMock(return_value=True),
)
@mock.patch(
    "src.api.routes.order.fastapi.BackgroundTasks.add_task",
    return_value=AsyncMock(return_value=None),
)
@pytest.mark.asyncio
async def test_crud_orders(
    mock_is_product_updated: AsyncMock,
    mock_add_task: AsyncMock,
    async_authenticated_client: httpx.AsyncClient,
    api_order_url: str,
) -> None:
    response_get_multiple_order_for_user = await async_authenticated_client.get(
        api_order_url
    )
    response_get_multiple_orders_json = (
        response_get_multiple_order_for_user.json()
    )
    assert response_get_multiple_orders_json == [
        {"date": "2024-03-24T10:10:00Z", "total_price": 99.99000000000001}
    ]

    response_get_multiple_order_for_user = await async_authenticated_client.get(
        api_order_url + "/admin/all"
    )
    assert response_get_multiple_order_for_user.status_code == 401

    response_get_multiple_orders_query = await async_authenticated_client.get(
        api_order_url,
        params={
            "min_cost": 60,
            "max_cost": 93,
            "order_by": "price",
        },
    )
    assert response_get_multiple_orders_query.json() == []

    response_delete_order = await async_authenticated_client.delete(
        api_order_url + "/1",
    )
    assert response_delete_order.status_code == 401

    response_create_order = await async_authenticated_client.post(
        api_order_url,
        json=[
            {"quantity": 1, "total": 25.99, "product_id": 1},
            {"quantity": 2, "total": 234.13, "product_id": 2},
        ],
        headers={"Content-Type": "application/json"},
    )
    response_create_order_json = response_create_order.json()

    assert response_create_order.status_code == 201
    assert response_create_order_json["total_price"] == 260.12
    assert response_create_order_json["user_id"] == 2
    assert response_create_order_json["id"] == 3


@pytest.mark.asyncio
async def test_crud_orders_w_admin_account(
    async_authenticated_client_admin: httpx.AsyncClient,
    api_order_url: str,
) -> None:
    response_get_multiple_order = await async_authenticated_client_admin.get(
        api_order_url + "/admin/all",
        params={
            "min_cost": 60,
            "max_cost": 93,
            "order_by": "price",
        },
    )
    assert response_get_multiple_order.status_code == 200
