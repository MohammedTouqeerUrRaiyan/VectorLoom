from fastapi import APIRouter

from src.api.routes.health import router as health_router
from src.api.routes.upload import router as upload_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    upload_router,
    prefix="/documents",
    tags=["Documents"]
)