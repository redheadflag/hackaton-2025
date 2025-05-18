import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from core.logging import setup_logging
from core.config import backend_settings


setup_logging()


logger = logging.getLogger(__name__)
logger.info(f"Application starts on port {backend_settings.port}")


app = FastAPI(
    title="Nature lovers",
    openapi_url=backend_settings.api_endpoint + "/openapi.json",
)


app.include_router(api_router, prefix=backend_settings.api_endpoint)


app.add_middleware(
    CORSMiddleware,
    allow_origins=backend_settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
