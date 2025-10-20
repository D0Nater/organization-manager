"""Application configuration."""

from pydantic import Field

from orgmgr.lib.configs import (
    BaseConfig,
    IdempotencyConfig,
    RedisConfig,
    SentryConfig,
    ServerConfig,
    SQLAlchemyConfig,
)


class AppConfig(BaseConfig):
    """Application configuration."""

    server: ServerConfig = Field(default_factory=ServerConfig)
    idempotency: IdempotencyConfig = Field(default_factory=IdempotencyConfig)
    database: SQLAlchemyConfig
    redis: RedisConfig
    sentry: SentryConfig = Field(default_factory=SentryConfig)
