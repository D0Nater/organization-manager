"""Sentry config."""

from pydantic import Field

from orgmgr.lib.configs.base import BaseConfig


class SentryConfig(BaseConfig):
    """Sentry config.

    This config is used to configure the sentry.

    Attributes:
        url (str | None): The url of the sentry. Defaults to None.
    """

    url: str | None = Field(default=None)
