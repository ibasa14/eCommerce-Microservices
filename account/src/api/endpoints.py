import fastapi
from src.api.routes.authentication import router as login_router

router = fastapi.APIRouter()

router.include_router(router=login_router)
