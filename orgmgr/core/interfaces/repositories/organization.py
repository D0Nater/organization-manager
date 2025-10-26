"""Organization repository."""

from typing import Protocol

from orgmgr.core.entities.organization import Organization
from orgmgr.core.types import OrganizationId


class OrganizationRepository(Protocol):
    """Protocol defining the interface for organization repositories."""

    async def create(self, organization: Organization) -> Organization:
        """Create a new organization entity.

        Args:
            organization (Organization): The organization entity to create.

        Returns:
            Organization: The created organization entity.
        """

    async def get_by_id(self, organization_id: OrganizationId) -> Organization | None:
        """Retrieve a single organization entity by its ID.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to retrieve.

        Returns:
            Organization | None: The retrieved organization entity, or None if not found.
        """

    async def update(self, organization: Organization) -> Organization:
        """Update an existing organization entity.

        Args:
            organization (Organization): The organization entity with updated values.

        Returns:
            Organization: The updated organization entity.
        """

    async def delete(self, organization_id: OrganizationId) -> None:
        """Delete an existing organization entity by its ID.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to delete.

        Returns:
            None
        """
