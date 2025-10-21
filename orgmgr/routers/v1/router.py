"""Version 1 API."""

from fastapi import APIRouter

from . import activity, building


router = APIRouter(prefix="/v1")
routers: list[APIRouter] = [
    activity.router,
    building.router,
]

for i in routers:
    router.include_router(i)
