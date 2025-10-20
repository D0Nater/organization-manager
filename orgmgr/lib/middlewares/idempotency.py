"""Idempotent request middleware."""

from collections.abc import Awaitable, Callable
from hashlib import sha256
from typing import Any

from cbor2 import dumps as cbor2_dumps, loads as cbor2_loads
from fastapi import Request, Response
from redis.asyncio import Redis
from starlette.concurrency import iterate_in_threadpool


class IdempotencyKeysStorage:
    """Middleware to handle idempotent requests using Redis for caching responses.

    This middleware checks for an 'X-Idempotency-Key' in the request headers and uses it to cache responses
    for POST, PUT, and PATCH requests. If a request with the same idempotency key is received, the cached
    response is returned instead of processing the request again.
    """

    allowed_methods = {"POST", "PUT", "PATCH"}
    _redis_key = "request:{key}"

    def __init__(self, redis: Redis, ttl: int = 120):
        """Initializes the IdempotencyKeysStorage with Redis client and TTL for cached responses.

        Args:
            redis (Redis): The Redis client instance used to store and retrieve cached responses.
            ttl (int): Time-to-live for cached responses in seconds. Defaults to 120 seconds.
        """
        self._redis = redis
        self._ttl = ttl

    async def handle_request(
        self, idempotency_key: str, request: Request, call_next: Callable[..., Awaitable[Any]]
    ) -> Response:
        """Handles the request by returning a cached response if available or storing the response in Redis.

        Args:
            idempotency_key (str): The key used to identify idempotent requests.
            request (Request): The incoming HTTP request object.
            call_next (Callable[..., Awaitable[Any]]): The next middleware or endpoint callable.

        Returns:
            Response: The HTTP response, either from cache if available or freshly generated.
        """
        redis_key = await self.generate_redis_idempotency_key(request, idempotency_key)

        # Check if cached response exists
        if cached_response := await self._redis.get(redis_key):
            cached_data = cbor2_loads(cached_response)
            return Response(
                content=cached_data["body"],
                media_type=cached_data["headers"].get("content-type", "application/json"),
                headers={k: v for k, v in cached_data["headers"].items() if k.lower() != "content-type"},
                status_code=cached_data["status_code"],
            )

        # Process the request
        response = await call_next(request)

        # Cache the response if it is successful
        if response.status_code < 400:
            await self.cache_response(redis_key, response)

        return response

    async def generate_redis_idempotency_key(self, request: Request, idempotency_key: str) -> str:
        """Generates a Redis key for the request based on method, path, body, and idempotency key.

        Args:
            request (Request): The incoming HTTP request object.
            idempotency_key (str): The idempotency key from request headers.

        Returns:
            str: A formatted Redis key unique to the request and idempotency key.
        """
        request_body = await request.body()
        key = sha256(
            request.method.encode() + request.url.path.encode() + request_body + idempotency_key.encode()
        ).hexdigest()
        return self._redis_key.format(key=key)

    async def cache_response(self, redis_key: str, response: Any) -> None:
        """Caches the HTTP response in Redis under the given key with a configured TTL.

        Args:
            redis_key (str): The Redis key under which the response will be stored.
            response (Any): The HTTP response object to cache.

        Returns:
            None
        """
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))

        response_body_bytes = b"".join(response_body)
        # Prepare data for caching
        cached_data = {
            "body": response_body_bytes,
            "headers": dict(response.headers),
            "status_code": response.status_code,
        }
        # Encode and store in Redis
        await self._redis.set(redis_key, cbor2_dumps(cached_data), ex=self._ttl)


async def idempotency_middleware(
    request: Request,
    call_next: Callable[..., Awaitable[Any]],
    idempotency_keys_storage: IdempotencyKeysStorage,
) -> Any:
    """Processes the incoming request and enforces idempotency using Redis-backed storage.

    If an 'X-Idempotency-Key' header is present and the method is POST, PUT, or PATCH, the response is either
    returned from cache or freshly processed and then cached. Other requests bypass idempotency handling.

    Args:
        request (Request): The incoming HTTP request object.
        call_next (Callable[..., Awaitable[Any]]): The next middleware or endpoint callable.
        idempotency_keys_storage (IdempotencyKeysStorage): Storage handler for idempotency keys and cached responses.

    Returns:
        Any: The HTTP response, either from cache or freshly generated.
    """
    idempotency_key = request.headers.get("X-Idempotency-Key")

    if not (idempotency_key and request.method in idempotency_keys_storage.allowed_methods):
        return await call_next(request)

    return await idempotency_keys_storage.handle_request(idempotency_key, request, call_next)
