"""Application dependencies."""

from dishka import AsyncContainer, make_async_container

from orgmgr.dependencies.action import ActionProvider
from orgmgr.dependencies.config import ConfigProvider
from orgmgr.dependencies.query import QueryProvider
from orgmgr.dependencies.repository import RepositoryProvider
from orgmgr.dependencies.service import ServiceProvider
from orgmgr.lib.dependencies import IdempotencyProvider, RedisProvider, SQLAlchemyProvider


def create_dishka_container() -> AsyncContainer:
    """Creates and configures the Dishka asynchronous dependency injection container.

    The container is initialized with providers for configuration, database, Redis, idempotency, repositories,
    queries, actions, and services, making them available for dependency resolution throughout the application.

    Returns:
        AsyncContainer: A fully configured asynchronous Dishka container.
    """
    return make_async_container(
        ConfigProvider(),
        SQLAlchemyProvider(),
        RedisProvider(),
        IdempotencyProvider(),
        RepositoryProvider(),
        QueryProvider(),
        ActionProvider(),
        ServiceProvider(),
    )
