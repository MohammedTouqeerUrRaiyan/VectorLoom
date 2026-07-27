from fastapi import FastAPI

from src.core.config import settings
from src.api.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Context-Aware Neural Recommendation Engine"
)

app.include_router(
    api_router,
    prefix=settings.API_PREFIX
)


@app.get("/")
async def root():
    return {
        "project": "VectorLoom",
        "status": "Running"
    }