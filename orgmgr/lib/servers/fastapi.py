"""Module containing main FastAPI application."""

from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from dishka import AsyncContainer as DishkaAsyncContainer, Scope
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from orgmgr.lib.configs import SentryConfig, ServerConfig
from orgmgr.lib.exceptions.handler import register_exception_handlers
from orgmgr.lib.middlewares import RequestIdMiddleware, idempotency_middleware
from orgmgr.lib.middlewares.idempotency import IdempotencyKeysStorage
from orgmgr.lib.utils.openapi import get_openapi
from orgmgr.lib.utils.sentry import configure_sentry


class FastAPIApp:
    """Wrapper for configuring and managing a FastAPI application instance."""

    def __init__(self, config: ServerConfig, app: FastAPI, dishka_container: DishkaAsyncContainer) -> None:
        """Initializes the FastAPI application wrapper.

        Args:
            config (ServerConfig): Application configuration object containing server settings.
            app (FastAPI): The FastAPI application instance. If an existing app is provided, it will be used as-is.
            dishka_container (DishkaAsyncContainer): The Dishka asynchronous dependency injection container.
        """
        self._server_config = config
        self._app = app
        self._dishka_container = dishka_container

    @property
    def fastapi_app(self) -> FastAPI:
        """Returns the underlying FastAPI application instance.

        Returns:
            FastAPI: The FastAPI application.
        """
        return self._app

    def include_router(self, router: APIRouter) -> None:
        """Includes a router in the FastAPI application.

        Args:
            router (APIRouter): A FastAPI APIRouter instance to be included.
        """
        self._app.include_router(router)

    def setup_dishka(self) -> None:
        """Sets up Dishka integration for the FastAPI application."""
        setup_dishka_fastapi(self._dishka_container, self._app)

    def setup_exception_handlers(self) -> None:
        """Registers global exception handlers for the FastAPI application."""
        register_exception_handlers(self._app)

    def setup_request_id_middleware(self) -> None:
        """Adds middleware for generating and attaching request IDs to requests."""
        self._app.add_middleware(RequestIdMiddleware)

    def setup_idempotency_middleware(self) -> None:
        """Adds middleware for enforcing idempotency in HTTP requests using Redis-backed storage."""

        @self._app.middleware("http")
        async def idempotency_middleware_for_app(
            request: Request,
            call_next: Callable[[Request], Awaitable[Response]],
        ) -> Response:
            """Enforces idempotency for incoming HTTP requests within the application.

            Args:
                request (Request): The incoming HTTP request.
                call_next (Callable[[Request], Awaitable[Response]]): The next middleware or endpoint callable.

            Returns:
                Response: The HTTP response, either from cache or freshly processed.
            """
            async with self._dishka_container(scope=Scope.REQUEST) as nested_container:
                return await idempotency_middleware(
                    request,
                    call_next,
                    await nested_container.get(IdempotencyKeysStorage),
                )

    def setup_cors_middleware(self) -> None:
        """Adds CORS middleware to the FastAPI application based on server configuration."""
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=self._server_config.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_sentry(self, config: SentryConfig) -> None:
        """Configures Sentry for error monitoring and reporting.

        Args:
            config (SentryConfig): The Sentry configuration containing the DSN URL.
        """
        configure_sentry(config.url)

    def setup_lifespan(self) -> None:
        """Sets up the application's lifespan context to manage startup and shutdown events."""

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
            """Defines the FastAPI lifespan context manager for setup and teardown operations.

            Args:
                app (FastAPI): The FastAPI application instance.

            Yields:
                None: Control to the application while it is running.
            """
            yield
            await app.state.dishka_container.close()

        self._app.router.lifespan_context = lifespan

    def override_openapi_schema(self) -> None:
        """Overrides the default OpenAPI schema with a customized version for the application."""
        self._app.openapi_schema = get_openapi(
            title=self._app.title,
            description=self._app.description,
            version=self._app.version,
            routes=self._app.routes,
            exclude_tags=["internal", "debug"] if self._server_config.production else [],
        )
