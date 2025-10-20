"""Module containing main FastAPI application."""

from fastapi import FastAPI

from orgmgr.config import AppConfig
from orgmgr.dependencies import create_dishka_container
from orgmgr.lib.servers.fastapi import FastAPIApp
from orgmgr.lib.utils.openapi import generate_operation_id
from orgmgr.routers import router
from orgmgr.version import __version__


def app() -> FastAPI:
    """Creates and configures a fully initialized FastAPI application instance for the Organization Manager service.

    This function serves as the main application entry point for Uvicorn. It loads environment-based configuration,
    initializes dependency containers, registers routers, sets up middleware, exception handlers, Sentry integration,
    OpenAPI schema customization, and application lifespan events.

    Returns:
        FastAPI: A fully configured and ready-to-run FastAPI application instance.
    """
    config = AppConfig.from_env()
    fastapi = FastAPI(
        title="Organization manager",
        description="Organization manager API.",
        version=__version__,
        generate_unique_id_function=generate_operation_id,
    )
    dishka_container = create_dishka_container()
    app = FastAPIApp(config.server, fastapi, dishka_container)

    app.include_router(router)
    app.setup_dishka()
    app.setup_exception_handlers()
    app.setup_request_id_middleware()
    app.setup_idempotency_middleware()
    app.override_openapi_schema()
    app.setup_sentry(config.sentry)
    app.setup_lifespan()

    return app.fastapi_app
