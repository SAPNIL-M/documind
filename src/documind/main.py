from fastapi import FastAPI

from documind.api.health import router as health_router

app = FastAPI(title="DocuMind")
app.include_router(health_router)
