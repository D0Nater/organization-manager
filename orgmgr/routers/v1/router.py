"""Version 1 API."""

from fastapi import APIRouter


router = APIRouter(prefix="/v1")
routers: list[APIRouter] = []

for i in routers:
    router.include_router(i)
