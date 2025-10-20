"""Common schemas for the API."""

from .base import BaseSchema


class OKSchema(BaseSchema):
    """OK schema."""

    ok: bool = True
