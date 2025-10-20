"""Request id middleware."""

from collections.abc import Awaitable, Callable
from typing import Any
from uuid import uuid4

from fastapi import Request
from sentry_sdk import configure_scope
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware that generates a unique request ID (UUID4) and attaches it to the request state for error tracking."""

    async def dispatch(self, request: Request, call_next: Callable[..., Awaitable[Any]]) -> Any:
        """Generates a UUID4 request ID, attaches it to the request state, and adds it to the Sentry scope.

        Args:
            request (Request): The incoming HTTP request object.
            call_next (Callable[..., Awaitable[Any]]): The next middleware or endpoint callable.

        Returns:
            Any: The HTTP response returned by the next middleware or endpoint.
        """
        # Generate a new UUID4
        request_id = uuid4()

        # Set the request_id in the state so that it can be accessed later
        request.state.request_id = request_id

        # Set the request_id in Sentry scope
        with configure_scope() as scope:
            scope.set_tag("request_id", request_id.hex)

        # Call the next middleware
        return await call_next(request)
