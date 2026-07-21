from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {
        "project": "VectorLoom",
        "status": "Running",
        "version": "1.0.0"
    }


@router.get("/health")
async def health():
    return {
        "status": "healthy"
    }