import fastapi
from typing import List, Dict
from src.api.dependencies.repository import get_repository
from src.api.dependencies.authentication import get_current_active_user
import src.data.schemas.order as OrderSchema
import src.data.schemas.user as UserSchema
from src.data.models import Order
from src.crud.order import OrderCRUD
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)
from src.constants import ORDER_ROUTER_URL
from typing import Annotated
from enum import Enum

router = fastapi.APIRouter(prefix=ORDER_ROUTER_URL, tags=["order"])


class OrderingEnum(str, Enum):
    name = "name"
    price = "price"


class OrderingType(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get(
    path="",
    name="orders:get-multiple-order",
    response_model=List[OrderSchema.OrderInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_order(
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["order:read"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
    categories: Annotated[
        str,
        fastapi.Query(
            title="Order Category",
            description="Identifier for the specific category",
            examples="1,2,3",
        ),
    ] = None,
    order_by: Annotated[
        OrderingEnum,
        fastapi.Query(
            title="Order ordering",
            description="Set the parameter use to order",
        ),
    ] = None,
    order_type: Annotated[
        OrderingType,
        fastapi.Query(
            title="Order ordering type",
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
) -> List[OrderSchema.OrderInResponse]:
    db_orders = await order_crud.get_multiple(
        categories=categories,
        order_by=order_by,
        order_type=order_type,
        min_cost=min_cost,
        max_cost=max_cost,
    )
    db_orders_list: list = list()

    for db_order in db_orders:
        order = OrderSchema.OrderInResponse(**db_order.to_dict())
        db_orders_list.append(order)

    return db_orders_list


@router.get(
    path="/{id}",
    name="orders:get-order",
    response_model=OrderSchema.OrderInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_order(
    id: int,
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["order:read"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
) -> OrderSchema.OrderInResponse:
    try:
        db_order = await order_crud.get(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return OrderSchema.OrderInResponse(**db_order.to_dict())


@router.post(
    path="",
    name="orders:post-order",
    response_model=OrderSchema.OrderInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_order(
    order_create: OrderSchema.OrderInCreate,
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["order:create"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
) -> OrderSchema.OrderInResponse:
    created_order = await order_crud.create_order(order_create=order_create)

    return OrderSchema.OrderInResponse(**created_order.to_dict())


@router.put(
    path="/{id}",
    name="orders:update-order",
    response_model=OrderSchema.OrderInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_order(
    id: int,
    order_in_update: OrderSchema.OrderInUpdate,
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["order:update"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
) -> OrderSchema.OrderInResponse:
    try:
        updated_db_order = await order_crud.update_order(
            id=id, order_update=order_in_update
        )

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return OrderSchema.OrderInResponse(**updated_db_order.to_dict())


@router.delete(
    path="/{id}",
    name="orders:delete-order",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_order(
    id: int,
    current_user: Annotated[
        UserSchema.User,
        fastapi.Security(get_current_active_user, scopes=["order:delete"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
) -> Dict[str, str]:
    try:
        deletion_result = await order_crud.delete(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
