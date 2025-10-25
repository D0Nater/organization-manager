"""Organization activity repository."""

from collections.abc import Iterable
from typing import Protocol

from orgmgr.core.types import ActivityId, OrganizationId


class OrganizationActivityRepository(Protocol):
    """Protocol defining the interface for organization activities repositories."""

    async def create(self, organization_id: OrganizationId, activity_ids: Iterable[ActivityId]) -> None:
        """Create organization activities in the database.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization.
            activity_ids (Iterable[ActivityId]): An iterable of unique
                activity identifiers to associate with the organization.

        Returns:
            None
        """

    async def delete(
        self, organization_id: OrganizationId | None = None, activity_ids: Iterable[ActivityId] | None = None
    ) -> None:
        """Delete organization activities from the database.

        WARNING!!! IF BOTH organization_id AND activity_ids ARE None, ALL THE ORGANIZATION ACTIVITIES WILL BE DELETED!!!

        Args:
            organization_id (OrganizationId | None): The unique identifier of the organization. Defaults to None.
            activity_ids (Iterable[ActivityId] | None): An iterable of unique activity identifiers. Defaults to None.

        Returns:
            None
        """
