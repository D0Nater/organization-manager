"""Idempotency provider."""

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from orgmgr.lib.configs.idempotency import IdempotencyConfig
from orgmgr.lib.middlewares.idempotency import IdempotencyKeysStorage


class IdempotencyProvider(Provider):
    """Idempotency provider."""

    @provide(scope=Scope.REQUEST)
    async def idempotency_keys_storage(
        self, redis: Redis, idempotency_config: IdempotencyConfig
    ) -> IdempotencyKeysStorage:
        """Creates and returns an IdempotencyKeysStorage instance using Redis and configuration settings.

        Args:
            redis (Redis): The Redis client instance used for storing and retrieving idempotency keys.
            idempotency_config (IdempotencyConfig): Configuration containing settings such as TTL for idempotency keys.

        Returns:
            IdempotencyKeysStorage: An instance of IdempotencyKeysStorage initialized with Redis and the configured TTL.
        """
        return IdempotencyKeysStorage(redis, idempotency_config.ttl)
