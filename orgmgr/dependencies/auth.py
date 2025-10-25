"""Auth deps."""

from collections.abc import Callable
from typing import Annotated, Any

from dishka import AsyncContainer
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from orgmgr.services import AuthService


def require_auth() -> Callable[..., Any]:
    """Creates a dependency injection wrapper for authentication.

    Returns:
        Callable[..., Any]: An asynchronous wrapper function suitable for use as a FastAPI dependency.
    """

    async def wrapper(
        request: Request,
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
    ) -> None:
        """The actual dependency injection wrapper that performs the authentication logic.

        Args:
            request (Request): The incoming request object.
            credentials (Annotated[HTTPAuthorizationCredentials | None, Depends]):
                Optional HTTP authorization credentials from the request header.
                `auto_error=False` is used to suppress automatic FastAPI error handling.

        Raises:
            ForbiddenException: If authentication is enabled and the provided token is invalid.
        """
        dishka_container: AsyncContainer = request.app.state.dishka_container

        async with dishka_container() as d:
            auth_service = await d.get(AuthService)

            if not auth_service.is_disable():
                credentials_: HTTPAuthorizationCredentials = await HTTPBearer()(request)  # type: ignore[assignment]
                await auth_service.authenticate_from_token(credentials_.credentials)

    return wrapper
