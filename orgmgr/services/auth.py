"""Auth service."""

from secrets import compare_digest

from orgmgr.lib.configs import AuthConfig
from orgmgr.lib.exceptions.base import ForbiddenException


class AuthService:
    """Service layer for auth."""

    def __init__(self, auth_config: AuthConfig):
        """Initialize the auth service.

        Args:
            auth_config (AuthConfig): Auth config.
        """
        self._auth_config = auth_config

    def is_disable(self) -> bool:
        """Checks if authentication is disabled.

        Returns:
            bool: True if auth is disabled, False otherwise.
        """
        return self._auth_config.disable

    async def authenticate_from_token(self, token: str) -> None:
        """Authenticates a request using a provided token.

        Args:
            token (str): The token containing the API key payload to be authenticated.

        Raises:
            ForbiddenException: If the provided token does not match the configured token.
        """
        if self._auth_config.disable:
            return

        if not compare_digest(token, self._auth_config.token):
            raise ForbiddenException("Invalid token")
