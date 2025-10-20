"""Base config."""

from logging import getLogger
from os import environ
from typing import Any, Self

from pydantic_settings import BaseSettings, SettingsConfigDict


logger = getLogger(__name__)


class BaseConfig(BaseSettings):
    """Base configuration class for application settings.

    Provides common configuration behavior for all config classes,
    including environment variable parsing and logging on initialization.
    """

    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_nested_delimiter="__", extra="ignore")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize configuration instance.

        Args:
            *args (Any): Positional arguments passed to `BaseSettings`.
            **kwargs (Any): Keyword arguments passed to `BaseSettings`.
        """
        super().__init__(*args, **kwargs)
        logger.debug(f"Config initialized: {self.model_dump()}")

    @classmethod
    def from_env(cls) -> Self:
        """Create configuration from environment variables and secrets directory.

        Reads environment variables from a `.env` file (default: `.env`) and optionally
        from a secrets directory if `SECRETS_DIR` is set.

        Returns:
            Self: A new configuration instance loaded from environment variables.
        """
        return cls(_env_file=environ.get("ENV_FILE", ".env"), _secrets_dir=environ.get("SECRETS_DIR"))
