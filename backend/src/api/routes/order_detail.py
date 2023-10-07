import fastapi
from typing import List, Dict
from src.api.dependencies.repository import get_repository
import src.data.schemas.order_detail as OrderDetailSchema
from src.data.models import OrderDetail
from src.crud.order_detail import OrderDetailCRUD
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)
from src.constants import ORDER_DETAIL_ROUTER_URL


router = fastapi.APIRouter(
    prefix=ORDER_DETAIL_ROUTER_URL, tags=["order_detail"]
)


@router.get(
    path="",
    name="order_details:get-multiple-order_details",
    response_model=List[OrderDetailSchema.OrderDetailInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_multiple_order_detail(
    order_detail_crud: OrderDetailCRUD = fastapi.Depends(
        get_repository(repo_type=OrderDetailCRUD, model=OrderDetail)
    ),
) -> List[OrderDetailSchema.OrderDetailInResponse]:
    db_order_details = await order_detail_crud.get_multiple()
    db_order_details_list: list = list()

    for db_order_detail in db_order_details:
        order_detail = OrderDetailSchema.OrderDetailInResponse(
            **db_order_detail.to_dict()
        )
        db_order_details_list.append(order_detail)

    return db_order_details_list


@router.get(
    path="/{id}",
    name="order_details:get-order_detail",
    response_model=OrderDetailSchema.OrderDetailInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_order_detail(
    id: int,
    order_detail_crud: OrderDetailCRUD = fastapi.Depends(
        get_repository(repo_type=OrderDetailCRUD, model=OrderDetail)
    ),
) -> OrderDetailSchema.OrderDetailInResponse:
    try:
        db_order_detail = await order_detail_crud.get(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return OrderDetailSchema.OrderDetailInResponse(**db_order_detail.to_dict())


@router.post(
    path="",
    name="order_details:post-order_detail",
    response_model=List[OrderDetailSchema.OrderDetailInResponse],
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_order_detail(
    order_detail_create_list: List[OrderDetailSchema.OrderDetailInput],
    order_detail_crud: OrderDetailCRUD = fastapi.Depends(
        get_repository(repo_type=OrderDetailCRUD, model=OrderDetail)
    ),
) -> List[OrderDetailSchema.OrderDetailInResponse]:
    created_order_detail = await order_detail_crud.create_order_detail(
        order_detail_create_list=order_detail_create_list
    )
    return created_order_detail

@router.put(
    path="/{id}",
    name="order_details:update-order_detail",
    response_model=OrderDetailSchema.OrderDetailInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_order_detail(
    id: int,
    order_detail_in_update: OrderDetailSchema.OrderDetailInUpdate,
    order_detail_crud: OrderDetailCRUD = fastapi.Depends(
        get_repository(repo_type=OrderDetailCRUD, model=OrderDetail)
    ),
) -> OrderDetailSchema.OrderDetailInResponse:
    try:
        updated_db_order_detail = await order_detail_crud.update_order_detail(
            id=id, order_detail_update=order_detail_in_update
        )

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return OrderDetailSchema.OrderDetailInResponse(
        **updated_db_order_detail.to_dict()
    )


@router.delete(
    path="/{id}",
    name="order_details:delete-order_detail",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_order_detail(
    id: int,
    order_detail_crud: OrderDetailCRUD = fastapi.Depends(
        get_repository(repo_type=OrderDetailCRUD, model=OrderDetail)
    ),
) -> Dict[str, str]:
    try:
        deletion_result = await order_detail_crud.delete(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
