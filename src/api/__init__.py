from fastapi import APIRouter

from api import channels, messages, users


api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(channels.router, tags=["channels"])
api_router.include_router(messages.router, tags=["messages"])
