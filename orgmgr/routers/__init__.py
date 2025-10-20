"""Module containing all FastAPI routes."""

from fastapi import APIRouter

from .ping import router as ping_router
from .v1 import router as v1_router


router = APIRouter(prefix="/api")
router.include_router(ping_router)
router.include_router(v1_router.router)
