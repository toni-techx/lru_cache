from fastapi import FastAPI

from api.api import router as api_router
from app.config import settings
from app.core import logger
from app.middleware import log_middleware

app = FastAPI()
app.middleware("http")(log_middleware)
app.include_router(api_router)

# initialize_cache()

logger.info("Application startup with host: %s, port: %s", settings.app_host, settings.app_port)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
