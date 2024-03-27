import httpx
import pytest
from src.constants import DEFAULT_PNG_NAME, PRODUCT_ROUTER_URL
from typing import Dict, Any
from unittest import mock
from dataclasses import dataclass
import pydantic


@pytest.fixture
def api_product_url(api_url) -> str:
    return f"{api_url}{PRODUCT_ROUTER_URL}"


@pytest.mark.asyncio
async def test_crud_products_non_authenticated(
    async_non_authenticated_client: httpx.AsyncClient,
    api_product_url: str,
) -> None:
    response_get_multiple_products = await async_non_authenticated_client.get(
        api_product_url
    )
    assert response_get_multiple_products.status_code == 401

    response_get_product = await async_non_authenticated_client.get(
        api_product_url + "/1",
    )
    assert response_get_product.status_code == 401

    response_create_product = await async_non_authenticated_client.post(
        api_product_url,
        json={
            "name": "product3",
            "description": "description3",
            "price": 923.1223,
            "stock": 25,
            "category_id": 3,
        },
        headers={"Content-Type": "application/json"},
    )
    assert response_create_product.status_code == 401

    response_update_product = await async_non_authenticated_client.put(
        api_product_url + "/1",
        json={
            "name": "product3_mod",
            "description": "description3_mod",
            "picture": DEFAULT_PNG_NAME,
            "price": 1,
            "stock": 1,
            "category_id": 5,
        },
        headers={"Content-Type": "application/json"},
    )
    assert response_update_product.status_code == 401

    response_delete_product = await async_non_authenticated_client.delete(
        api_product_url + "/1",
    )
    assert response_delete_product.status_code == 401


@pytest.mark.asyncio
async def test_crud_products(
    async_authenticated_client: httpx.AsyncClient,
    api_product_url: str,
) -> None:
    response_get_multiple_products = await async_authenticated_client.get(
        api_product_url
    )
    response_get_multiple_products_json = list(
        filter(lambda a: a["id"] != 2, response_get_multiple_products.json())
    )
    assert response_get_multiple_products_json == [
        {
            "id": 1,
            "name": "product1",
            "description": "description1",
            "picture": DEFAULT_PNG_NAME,
            "price": 59.99,
            "stock": 100,
            "category_id": 1,
        },
        {
            "id": 3,
            "name": "product_22",
            "description": "description22",
            "picture": DEFAULT_PNG_NAME,
            "price": 92.59,
            "stock": 200,
            "category_id": 3,
        },
    ]
    response_get_multiple_products_query = await async_authenticated_client.get(
        api_product_url,
        params={
            "min_cost": 60,
            "max_cost": 93,
            "order_by": "price",
            "categories": "3",
        },
    )
    response_get_multiple_products_query_json = list(
        filter(
            lambda a: a["id"] != 2, response_get_multiple_products_query.json()
        )
    )
    assert response_get_multiple_products_query_json == [
        {
            "id": 3,
            "name": "product_22",
            "description": "description22",
            "picture": DEFAULT_PNG_NAME,
            "price": 92.59,
            "stock": 200,
            "category_id": 3,
        },
    ]

    response_delete_product = await async_authenticated_client.delete(
        api_product_url + "/1",
    )
    assert response_delete_product.status_code == 401

    response_create_product = await async_authenticated_client.post(
        api_product_url,
        json={
            "name": "product3",
            "description": "description3",
            "price": 923.1223,
            "stock": 25,
            "category_id": 3,
        },
        headers={"Content-Type": "application/json"},
    )
    assert response_create_product.status_code == 401

    response_create_product = await async_authenticated_client.put(
        api_product_url+"/inventory/substract",
        json=[{
            "id": 2,
            "quantity": 1,
        }],
        headers={"Content-Type": "application/json"},
    )
    assert response_create_product.status_code == 200
    assert response_create_product.json() == True

    response_create_product = await async_authenticated_client.put(
        api_product_url+"/inventory/substract",
        json=[{
            "id": 2,
            "quantity": 5,
        }],
        headers={"Content-Type": "application/json"},
    )
    assert response_create_product.status_code == 200
    assert response_create_product.json() == False


@pytest.mark.asyncio
async def test_crud_products_w_admin_account(
    async_authenticated_client_admin: httpx.AsyncClient,
    api_product_url: str,
) -> None:
    response_get_multiple_products = await async_authenticated_client_admin.get(
        api_product_url
    )
    response_get_multiple_products_json = list(
        filter(lambda a: a["id"] != 2, response_get_multiple_products.json())
    )
    assert response_get_multiple_products_json == [
        {
            "id": 1,
            "name": "product1",
            "description": "description1",
            "picture": DEFAULT_PNG_NAME,
            "price": 59.99,
            "stock": 100,
            "category_id": 1,
        },
        {
            "id": 3,
            "name": "product_22",
            "description": "description22",
            "picture": DEFAULT_PNG_NAME,
            "price": 92.59,
            "stock": 200,
            "category_id": 3,
        },
    ]
    response_get_multiple_products_query = (
        await async_authenticated_client_admin.get(
            api_product_url,
            params={
                "min_cost": 60,
                "max_cost": 93,
                "order_by": "price",
                "categories": "3",
            },
        )
    )
    response_get_multiple_products_query_json = list(
        filter(
            lambda a: a["id"] != 2, response_get_multiple_products_query.json()
        )
    )
    assert response_get_multiple_products_query_json == [
        {
            "id": 3,
            "name": "product_22",
            "description": "description22",
            "picture": DEFAULT_PNG_NAME,
            "price": 92.59,
            "stock": 200,
            "category_id": 3,
        },
    ]

    response_delete_product = await async_authenticated_client_admin.delete(
        api_product_url + "/1",
    )
    assert response_delete_product.status_code == 200

    response_after_deletion = await async_authenticated_client_admin.get(
        api_product_url
    )
    response_after_deletion_json = list(
        filter(lambda a: a["id"] != 2, response_after_deletion.json())
    )

    assert response_after_deletion_json == [
        {
            "id": 3,
            "name": "product_22",
            "description": "description22",
            "picture": DEFAULT_PNG_NAME,
            "price": 92.59,
            "stock": 200,
            "category_id": 3,
        },
    ]
    response_create_product = await async_authenticated_client_admin.post(
        api_product_url,
        json={
            "name": "product3",
            "description": "description3",
            "price": 923.1223,
            "stock": 25,
            "category_id": 3,
        },
        headers={"Content-Type": "application/json"},
    )
    assert response_create_product.json() == {
        "id": 4,
        "name": "product3",
        "description": "description3",
        "picture": DEFAULT_PNG_NAME,
        "price": 923.1223,
        "stock": 25,
        "category_id": 3,
    }

    response_get_multiple_products_2 = (
        await async_authenticated_client_admin.get(api_product_url)
    )
    response_get_multiple_products_2_json = list(
        filter(lambda a: a["id"] != 2, response_get_multiple_products_2.json())
    )

    assert response_get_multiple_products_2_json == [
        {
            "id": 3,
            "name": "product_22",
            "description": "description22",
            "picture": DEFAULT_PNG_NAME,
            "price": 92.59,
            "stock": 200,
            "category_id": 3,
        },
        {
            "id": 4,
            "name": "product3",
            "description": "description3",
            "picture": DEFAULT_PNG_NAME,
            "price": 923.1223,
            "stock": 25,
            "category_id": 3,
        },
    ]
    response_update_product = await async_authenticated_client_admin.put(
        api_product_url + "/4",
        json={
            "name": "product3_mod",
            "description": "description3_mod",
            "picture": DEFAULT_PNG_NAME,
            "price": 1,
            "stock": 1,
            "category_id": 5,
        },
        headers={"Content-Type": "application/json"},
    )
    assert response_update_product.json() == {
        "id": 4,
        "name": "product3_mod",
        "description": "description3_mod",
        "picture": DEFAULT_PNG_NAME,
        "price": 1,
        "stock": 1,
        "category_id": 5,
    }
    response_get_product = await async_authenticated_client_admin.get(
        api_product_url + "/4",
    )
    assert response_get_product.json() == {
        "id": 4,
        "name": "product3_mod",
        "description": "description3_mod",
        "picture": DEFAULT_PNG_NAME,
        "price": 1,
        "stock": 1,
        "category_id": 5,
    }
