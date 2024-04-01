from enum import Enum
from typing import Annotated, Dict, List

import fastapi
import httpx
import src.data.schemas.jwt as JWTSchema
import src.data.schemas.order as OrderSchema
import src.data.schemas.order_detail as OrderDetailSchema
from src.api.dependencies.authentication import get_current_active_user
from src.api.dependencies.repository import get_repository
from src.celery_worker import send_email
from src.constants import ORDER_ROUTER_URL
from src.crud.order import OrderCRUD
from src.data.models import Order
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)
from src.utilities.exceptions.http.exc_409 import (
    http_409_exc_conflict_not_available_product,
)

router = fastapi.APIRouter(prefix=ORDER_ROUTER_URL, tags=["order"])


class OrderingEnum(str, Enum):
    date = "date"
    price = "price"


class OrderingType(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get(
    path="",
    name="orders:get-multiple-order-for-user",
    response_model=List[OrderSchema.Order],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_order_for_user(
    current_user: Annotated[
        JWTSchema.JWTUser,
        fastapi.Security(get_current_active_user, scopes=["order:read"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
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
) -> List[OrderSchema.Order]:
    db_orders = await order_crud.get_multiple(
        users_id=[current_user.id],
        order_by=order_by,
        order_type=order_type,
        min_cost=min_cost,
        max_cost=max_cost,
    )
    db_orders_list: list = list()
    for db_order in db_orders:
        order = OrderSchema.Order(**db_order.to_dict())
        db_orders_list.append(order)
    return db_orders_list


@router.get(
    path="/admin/all",
    name="orders:get-multiple-order",
    response_model=List[OrderSchema.Order],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_order(
    current_user: Annotated[
        JWTSchema.JWTUser,
        fastapi.Security(get_current_active_user, scopes=["order:read-all"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
    users_id: Annotated[
        str,
        fastapi.Query(
            title="Order ordering",
            description="Set the users from which to extract orders",
            examples={"users_id": "1,2,3"},
        ),
    ] = "",
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
) -> List[OrderSchema.Order]:
    db_orders = await order_crud.get_multiple(
        users_id=(
            [uid.strip() for uid in users_id.split(",")] if users_id else None
        ),
        order_by=order_by,
        order_type=order_type,
        min_cost=min_cost,
        max_cost=max_cost,
    )
    db_orders_list: list = list()
    for db_order in db_orders:
        order = OrderSchema.Order(**db_order.to_dict())
        db_orders_list.append(order)
    return db_orders_list


@router.get(
    path="/{id}",
    name="orders:get-order",
    response_model=OrderSchema.OrderWithDetails,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_order(
    id: int,
    current_user: Annotated[
        JWTSchema.JWTUser,
        fastapi.Security(get_current_active_user, scopes=["order:read"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
) -> OrderSchema.OrderWithDetails:
    try:
        db_order = await order_crud.get(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    details = [
        OrderDetailSchema.OrderDetailForSpecificOrder(**detail.to_dict())
        for detail in db_order.order_details
    ]
    return OrderSchema.OrderWithDetails(
        **{
            "date": db_order.date,
            "total_price": db_order.total_price,
            "details": details,
        }
    )


@router.post(
    path="",
    name="orders:post-order",
    response_model=OrderSchema.OrderDB,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_order(
    order_in_create: List[OrderDetailSchema.OrderDetailForSpecificOrder],
    background_tasks: fastapi.BackgroundTasks,
    current_user: Annotated[
        JWTSchema.JWTUser,
        fastapi.Security(get_current_active_user, scopes=["order:create"]),
    ],
    order_crud: OrderCRUD = fastapi.Depends(
        get_repository(repo_type=OrderCRUD, model=Order)
    ),
) -> OrderSchema.OrderDB:
    try:
        created_order = await order_crud.create_order(
            order_create=order_in_create,
            user_id=current_user.id,
            token=current_user.token,
        )
    except httpx.HTTPStatusError:
        raise await http_409_exc_conflict_not_available_product()

    # Send email to user with the receipt
    background_tasks.add_task(
        send_email, current_user.email, "Order created successfully!"
    )
    return OrderSchema.OrderDB(**created_order.to_dict())


@router.delete(
    path="/{id}",
    name="orders:delete-order",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_order(
    id: int,
    current_user: Annotated[
        JWTSchema.JWTUser,
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
