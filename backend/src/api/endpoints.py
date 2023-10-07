import fastapi

from src.api.routes.user import router as user_router
from src.api.routes.product import router as product_router
from src.api.routes.order_detail import router as order_detail_router
from src.api.routes.order import router as order_router

router = fastapi.APIRouter()

router.include_router(router=user_router)
router.include_router(router=product_router)
router.include_router(router=order_detail_router)
router.include_router(router=order_router)
