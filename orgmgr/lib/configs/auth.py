"""Auth config."""

from typing import Self

from pydantic import Field, model_validator

from orgmgr.lib.configs.base import BaseConfig


class AuthConfig(BaseConfig):
    """Auth config.

    This config is used to configure the auth.
    """

    disable: bool = Field(default=False)
    token: str = Field(default="")

    @model_validator(mode="after")
    def validate_token_if_not_disabled(self) -> Self:
        """Validates that a token is present when authentication is enabled.

        This validator ensures that if disable is False, the token is not an empty string.

        Args:
            self (AuthConfig): The AuthConfig instance being validated.

        Returns:
            Self: The validated AuthConfig instance.

        Raises:
            ValueError: If disable is False and token is an empty string.
        """
        if self.disable is False and self.token == "":
            raise ValueError("Token is required when auth is not disabled")
        return self
