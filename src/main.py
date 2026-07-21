from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Context-Aware Neural Recommendation Engine",
    version=settings.APP_VERSION,
)


@app.get("/")
async def root():
    return {
        "project": "VectorLoom",
        "status": "Running",
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }