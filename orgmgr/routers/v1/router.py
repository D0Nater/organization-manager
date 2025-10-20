"""Version 1 API."""

from fastapi import APIRouter

from . import activity


router = APIRouter(prefix="/v1")
routers: list[APIRouter] = [
    activity.router,
]

for i in routers:
    router.include_router(i)
