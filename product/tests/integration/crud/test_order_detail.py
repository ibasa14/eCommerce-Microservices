# import httpx
# import pytest
# from src.constants import (
#     ORDER_DETAIL_ROUTER_URL,
#     ORDER_ROUTER_URL,
#     PRODUCT_ROUTER_URL,
#     DEFAULT_PNG_NAME,
# )


# @pytest.fixture
# def api_order_detail_url(api_url) -> str:
#     return f"{api_url}{ORDER_DETAIL_ROUTER_URL}"


# @pytest.fixture
# def api_order_url(api_url) -> str:
#     return f"{api_url}{ORDER_ROUTER_URL}"


# @pytest.fixture
# def api_product_url(api_url) -> str:
#     return f"{api_url}{PRODUCT_ROUTER_URL}"


# async def test_crud_order_details(
#     async_client: httpx.AsyncClient,
#     api_order_detail_url: str,
#     api_order_url: str,
#     api_product_url: str,
# ) -> None:
#     response_create_order_details = await async_client.post(
#         api_order_detail_url,
#         json=[{"product_id": 2, "quantity": 3}],
#         headers={"Content-Type": "application/json"},
#     )
#     assert response_create_order_details.status_code == 201
#     assert response_create_order_details.json() == [
#         {"id": 1, "total": 66, "order_id": 1, "product_id": 2, "quantity": 3}
#     ]

#     response_get_order = await async_client.get(
#         api_order_url + "/1",
#     )
#     response_get_order_json = response_get_order.json()
#     response_get_order_json.pop("date")
#     assert response_get_order_json == {"id": 1, "user_id": 2, "total": 66}

#     response_get_product = await async_client.get(
#         api_product_url + "/2",
#     )
#     assert response_get_product.json() == {
#         "id": 2,
#         "name": "product2",
#         "description": "description2",
#         "picture": DEFAULT_PNG_NAME,
#         "price": 22,
#         "stock": 2,
#         "category_id": 2,
#     }
