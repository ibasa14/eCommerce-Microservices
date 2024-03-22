import fastapi

from order.src.api.routes.order_ import router as order_router

router = fastapi.APIRouter()

router.include_router(router=order_router)
