import fastapi

from src.api.routes.user import router as user_router
from src.api.routes.product import router as product_user

router = fastapi.APIRouter()

router.include_router(router=user_router)
router.include_router(router=product_user)
