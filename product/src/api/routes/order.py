# import fastapi
# from typing import List, Dict
# from src.api.dependencies.repository import get_repository
# import src.data.schemas.order as OrderSchema
# from src.data.models import Order
# from src.crud.order import OrderCRUD
# from src.utilities.exceptions.database import EntityDoesNotExist
# from src.utilities.exceptions.http.exc_404 import (
#     http_404_exc_id_not_found_request,
# )
# from src.constants import ORDER_ROUTER_URL


# router = fastapi.APIRouter(prefix=ORDER_ROUTER_URL, tags=["order"])


# @router.get(
#     path="",
#     name="orders:get-multiple-orders",
#     response_model=List[OrderSchema.OrderInResponse],
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def get_multiple_order(
#     order_crud: OrderCRUD = fastapi.Depends(
#         get_repository(repo_type=OrderCRUD, model=Order)
#     ),
# ) -> List[OrderSchema.OrderInResponse]:
#     db_orders = await order_crud.get_multiple()
#     db_orders_list: list = list()

#     for db_order in db_orders:
#         order = OrderSchema.OrderInResponse(**db_order.to_dict())
#         db_orders_list.append(order)

#     return db_orders_list


# @router.get(
#     path="/{id}",
#     name="orders:get-order",
#     response_model=OrderSchema.OrderInResponse,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def get_order(
#     id: int,
#     order_crud: OrderCRUD = fastapi.Depends(
#         get_repository(repo_type=OrderCRUD, model=Order)
#     ),
# ) -> OrderSchema.OrderInResponse:
#     try:
#         db_order = await order_crud.get(id=id)

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=id)

#     return OrderSchema.OrderInResponse(**db_order.to_dict())


# @router.post(
#     path="",
#     name="orders:post-order",
#     response_model=List[OrderSchema.OrderInResponse],
#     status_code=fastapi.status.HTTP_201_CREATED,
# )
# async def create_order(
#     order_create_list: List[OrderSchema.OrderInCreate],
#     order_crud: OrderCRUD = fastapi.Depends(
#         get_repository(repo_type=OrderCRUD, model=Order)
#     ),
# ) -> List[OrderSchema.OrderInResponse]:
#     created_order = await order_crud.create_order(
#         order_create_list=order_create_list
#     )
#     return created_order


# @router.put(
#     path="/{id}",
#     name="orders:update-order",
#     response_model=OrderSchema.OrderInResponse,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def update_order(
#     id: int,
#     order_in_update: OrderSchema.OrderInUpdate,
#     order_crud: OrderCRUD = fastapi.Depends(
#         get_repository(repo_type=OrderCRUD, model=Order)
#     ),
# ) -> OrderSchema.OrderInResponse:
#     try:
#         updated_db_order = await order_crud.update_order(
#             id=id, order_update=order_in_update
#         )

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=id)

#     return OrderSchema.OrderInResponse(**updated_db_order.to_dict())


# @router.delete(
#     path="/{id}",
#     name="orders:delete-order",
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def delete_order(
#     id: int,
#     order_crud: OrderCRUD = fastapi.Depends(
#         get_repository(repo_type=OrderCRUD, model=Order)
#     ),
# ) -> Dict[str, str]:
#     try:
#         deletion_result = await order_crud.delete(id=id)

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=id)

#     return {"notification": deletion_result}
