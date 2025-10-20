"""Config provider."""

from dishka import Provider, Scope, provide

from orgmgr.config import AppConfig
from orgmgr.lib.configs.idempotency import IdempotencyConfig
from orgmgr.lib.configs.redis import RedisConfig
from orgmgr.lib.configs.sqlalchemy import SQLAlchemyConfig


class ConfigProvider(Provider):
    """Provider for application configuration objects."""

    @provide(scope=Scope.APP)
    def app_config(self) -> AppConfig:
        """Loads and returns the application configuration from environment variables.

        Returns:
            AppConfig: The main application configuration object.
        """
        return AppConfig.from_env()

    @provide(scope=Scope.APP)
    def idempotency_config(self, app_config: AppConfig) -> IdempotencyConfig:
        """Provides the idempotency configuration from the application config.

        Args:
            app_config (AppConfig): The main application configuration.

        Returns:
            IdempotencyConfig: The idempotency configuration.
        """
        return app_config.idempotency

    @provide(scope=Scope.APP)
    def sqlalchemy_config(self, app_config: AppConfig) -> SQLAlchemyConfig:
        """Provides the SQLAlchemy configuration from the application config.

        Args:
            app_config (AppConfig): The main application configuration.

        Returns:
            SQLAlchemyConfig: The SQLAlchemy database configuration.
        """
        return app_config.database

    @provide(scope=Scope.APP)
    def redis_config(self, app_config: AppConfig) -> RedisConfig:
        """Provides the Redis configuration from the application config.

        Args:
            app_config (AppConfig): The main application configuration.

        Returns:
            RedisConfig: The Redis configuration.
        """
        return app_config.redis
