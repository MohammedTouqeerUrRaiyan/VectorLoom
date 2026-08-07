from fastapi import APIRouter

from src.api.routes.health import router as health_router
from src.api.routes.upload import router as upload_router
from src.api.routes.chat import router as chat_router
from src.api.routes.chat_stream import router as chat_stream_router
from src.api.routes.chat_stream import router as chat_stream_router
from src.api.routes.document import router as document_router

api_router = APIRouter()

api_router.include_router(

    chat_stream_router,

    prefix="/chat",

    tags=["Streaming Chat"]

)

api_router.include_router(
    chat_stream_router,
    prefix="/chat",
    tags=["Chat Streaming"]
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    upload_router,
    prefix="/documents",
    tags=["Documents"]
)

api_router.include_router(document_router)