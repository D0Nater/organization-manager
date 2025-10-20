"""Redis config."""

from pydantic import Field, RedisDsn

from orgmgr.lib.configs.base import BaseConfig


class RedisConfig(BaseConfig):
    """Redis config.

    This config is used to configure the redis.

    Attributes:
        url (RedisDsn): The url of the redis. Defaults to "redis://localhost:6379".
    """

    url: RedisDsn = Field(default=RedisDsn("redis://localhost:6379"))
