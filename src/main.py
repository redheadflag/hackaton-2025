from fastapi import FastAPI
import uvicorn

from api import api_router
from core.logging import setup_logging


setup_logging()


app = FastAPI()


app.include_router(api_router)

