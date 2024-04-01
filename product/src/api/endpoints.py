import fastapi
from src.api.routes.product import router as product_router

router = fastapi.APIRouter()

router.include_router(router=product_router)
