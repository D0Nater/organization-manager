"""Server config."""

from pydantic import Field

from orgmgr.lib.configs.base import BaseConfig


class ServerConfig(BaseConfig):
    """Server config.

    This config is used to configure the server.

    Attributes:
        production (bool): The url of the server. Defaults to True.
        origins (list[str]): The origins of the server. Defaults to ["*"].
    """

    production: bool = Field(default=True)
    origins: list[str] = Field(default_factory=lambda: ["*"])
