from fastapi import FastAPI

from src.api.routes import chat
from src.api.routes import chat_stream
from src.api.routes import document
from src.api.routes import health
from src.api.routes import upload
from src.api.routes import recommendation

from src.config.settings import settings


# ==========================================================
# APPLICATION
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


# ==========================================================
# ROUTES
# ==========================================================

app.include_router(
    health.router,
    prefix=settings.API_PREFIX,
    tags=["Health"],
)

app.include_router(
    upload.router,
    prefix=settings.API_PREFIX,
    tags=["Upload"],
)

app.include_router(
    document.router,
    prefix=settings.API_PREFIX,
    tags=["Documents"],
)

app.include_router(
    chat.router,
    prefix=settings.API_PREFIX,
    tags=["Chat"],
)

app.include_router(
    chat_stream.router,
    prefix=settings.API_PREFIX,
    tags=["Chat Stream"],
)

app.include_router(
    recommendation.router,
    prefix=settings.API_PREFIX,
    tags=["Recommendations"],
)


# ==========================================================
# ROOT ENDPOINT
# ==========================================================

@app.get("/")
async def root():
    return {
        "project": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
    }