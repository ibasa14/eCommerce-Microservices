import fastapi
from typing import List, Dict
from src.api.dependencies.repository import get_repository
import src.data.schemas.product as ProductSchema
from src.data.models import Product
from src.crud.product import ProductCRUD
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)
from src.constants import PRODUCT_ROUTER_URL

router = fastapi.APIRouter(prefix=PRODUCT_ROUTER_URL, tags=["product"])


@router.get(
    path="",
    name="products:get-multiple-product",
    response_model=List[ProductSchema.ProductInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_product(
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> List[ProductSchema.ProductInResponse]:
    db_products = await product_crud.get_multiple()
    db_products_list: list = list()

    for db_product in db_products:
        product = ProductSchema.ProductInResponse(**db_product.to_dict())
        db_products_list.append(product)

    return db_products_list


@router.get(
    path="/{id}",
    name="products:get-product",
    response_model=ProductSchema.ProductInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_product(
    id: int,
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> ProductSchema.ProductInResponse:
    try:
        db_product = await product_crud.get(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return ProductSchema.ProductInResponse(**db_product.to_dict())


@router.post(
    path="",
    name="products:post-product",
    response_model=ProductSchema.ProductInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_product(
    product_create: ProductSchema.ProductInCreate,
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> ProductSchema.ProductInResponse:
    created_product = await product_crud.create_product(
        product_create=product_create
    )

    return ProductSchema.ProductInResponse(**created_product.to_dict())


@router.put(
    path="/{id}",
    name="products:update-product",
    response_model=ProductSchema.ProductInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_product(
    id: int,
    product_in_update: ProductSchema.ProductInUpdate,
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> ProductSchema.ProductInResponse:
    try:
        updated_db_product = await product_crud.update_product(
            id=id, product_update=product_in_update
        )

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return ProductSchema.ProductInResponse(**updated_db_product.to_dict())


@router.delete(
    path="/{id}",
    name="products:delete-product",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_product(
    id: int,
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> Dict[str, str]:
    try:
        deletion_result = await product_crud.delete(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
