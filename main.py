from fastapi import FastAPI
from api.endpoints import router as notification_router
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs"  # Автодок OpenAPI
)

app.include_router(notification_router)
