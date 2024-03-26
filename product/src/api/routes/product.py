import fastapi
from typing import List, Dict
from src.api.dependencies.repository import get_repository
from src.api.dependencies.authentication import get_current_active_user
import src.data.schemas.product as ProductSchema
import src.data.schemas.user as UserSchema
from src.data.models import Product
from src.crud.product import ProductCRUD
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)
from src.constants import PRODUCT_ROUTER_URL
from typing import Annotated
from enum import Enum

router = fastapi.APIRouter(prefix=PRODUCT_ROUTER_URL, tags=["product"])


class OrderingEnum(str, Enum):
    name = "name"
    price = "price"


class OrderingType(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get(
    path="",
    name="products:get-multiple-product",
    response_model=List[ProductSchema.ProductInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_product(
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["product:read"]),
    ],
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
    categories: Annotated[
        str,
        fastapi.Query(
            title="Product Category",
            description="Identifier for the specific category",
            examples="1,2,3",
        ),
    ] = None,
    order_by: Annotated[
        OrderingEnum,
        fastapi.Query(
            title="Product ordering",
            description="Set the parameter use to order",
        ),
    ] = None,
    order_type: Annotated[
        OrderingType,
        fastapi.Query(
            title="Product ordering type",
            description="Set the ordering approach",
        ),
    ] = OrderingType.asc,
    min_cost: Annotated[
        float,
        fastapi.Query(
            title="Min Cost", description="Set the minimum cost", ge=0
        ),
    ] = None,
    max_cost: Annotated[
        float,
        fastapi.Query(
            title="Max Cost", description="Set the maximum cost", ge=0
        ),
    ] = None,
) -> List[ProductSchema.ProductInResponse]:
    db_products = await product_crud.get_multiple(
        categories=categories,
        order_by=order_by,
        order_type=order_type,
        min_cost=min_cost,
        max_cost=max_cost,
    )
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
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["product:read"]),
    ],
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
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["product:create"]),
    ],
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
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["product:update"]),
    ],
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


@router.put(
    path="/inventory/substract",
    name="products:inventory-substract",
    status_code=fastapi.status.HTTP_200_OK,
)
async def inventory_substract(
    products_to_substract: List[ProductSchema.ProductToSubstract],
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["product:update"]),
    ],
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> bool:
    try:
        updated_db_product = await product_crud.subtract_from_inventory(
            products_to_substract
        )
        if updated_db_product:
            return True
        return False
    except Exception as e:
        print(f"Error updating product: {e}")
        return False


@router.delete(
    path="/{id}",
    name="products:delete-product",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_product(
    id: int,
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["product:delete"]),
    ],
    product_crud: ProductCRUD = fastapi.Depends(
        get_repository(repo_type=ProductCRUD, model=Product)
    ),
) -> Dict[str, str]:
    try:
        deletion_result = await product_crud.delete(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
