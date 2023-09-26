import fastapi

from src.api.routes.user import router as user_router

router = fastapi.APIRouter()

router.include_router(router=user_router)
