from fastapi import FastAPI

app = FastAPI(
    title="VectorLoom API",
    description="Context-Aware Neural Recommendation Engine",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "project": "VectorLoom",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }