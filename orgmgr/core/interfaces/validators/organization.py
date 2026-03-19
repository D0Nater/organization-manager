"""Organization validator interface."""

from typing import Protocol

from orgmgr.core.entities.organization import Organization
from orgmgr.core.types import OrganizationId


class OrganizationValidator(Protocol):
    """Protocol defining the interface for organization validation."""

    async def ensure_exists(self, organization_id: OrganizationId) -> Organization:
        """Ensure that a organization exists.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to validate.

        Returns:
            Organization: The validated organization entity.

        Raises:
            OrganizationNotFoundError: If no organization exists with the given ID.
        """
