import fastapi
from src.api.routes.order import router as order_router

router = fastapi.APIRouter()

router.include_router(router=order_router)
