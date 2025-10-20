"""Redis provider."""

from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from redis.asyncio import ConnectionPool, Redis

from orgmgr.lib.configs.redis import RedisConfig


class RedisProvider(Provider):
    """Redis provider."""

    @provide(scope=Scope.APP)
    def redis_pool(self, redis_config: RedisConfig) -> ConnectionPool:
        """Creates and returns a Redis connection pool from the given configuration for application-wide usage.

        Args:
            redis_config (RedisConfig): The Redis configuration object containing the connection URL.

        Returns:
            ConnectionPool: A Redis connection pool instance created from the provided configuration.
        """
        return ConnectionPool.from_url(str(redis_config.url))

    @provide(scope=Scope.REQUEST)
    async def redis(self, redis_pool: ConnectionPool) -> AsyncGenerator[Redis]:
        """Provides a Redis client instance using the given connection pool for the lifetime of a request.

        Args:
            redis_pool (ConnectionPool): The Redis connection pool to create the client from.

        Yields:
            Redis: A Redis client instance tied to the provided connection pool.
        """
        redis = Redis(connection_pool=redis_pool)
        try:
            yield redis
        finally:
            await redis.aclose()
