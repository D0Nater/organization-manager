"""Organization activity repository."""

from collections.abc import Iterable

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.core.interfaces.repositories.organization_activity import OrganizationActivityRepository
from orgmgr.core.types import ActivityId, OrganizationId
from orgmgr.models import OrganizationActivityModel


class SAOrganizationActivityRepository(OrganizationActivityRepository):
    """Protocol defining the interface for organization repositories."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        """
        self._session = session

    async def create(self, organization_id: OrganizationId, activity_ids: Iterable[ActivityId]) -> None:
        """Create organization activities in the database.

        Args:
            organization_id (organization_id): The IDs of the organizations to associate with the activities.
            activity_ids (Iterable[ActivityId]): The IDs of the activities to associate with the organizations.

        Returns:
            Sequence[ChatServiceModel]: The sequence of created ChatServiceModel objects.
        """
        if not activity_ids:
            return

        organization_activities = [
            OrganizationActivityModel(organization_id=organization_id, activity_id=activity_id)
            for activity_id in activity_ids
        ]

        self._session.add_all(organization_activities)
        await self._session.flush()

    async def delete(
        self, organization_id: OrganizationId | None = None, activity_ids: Iterable[ActivityId] | None = None
    ) -> None:
        """Delete organization activities from the database.

        WARNING!!! IF BOTH organization_id AND activity_ids ARE None, ALL THE ORGANIZATION ACTIVITIES WILL BE DELETED!!!

        Args:
            organization_id (Iterable[int] | None): The IDs of the organizations
                associated with the activities. Defaults to None.
            activity_ids (Iterable[int] | None): The IDs of the activities
                associated with the organizations. Defaults to None.

        Returns:
            None
        """
        stmt = delete(OrganizationActivityModel)

        if organization_id is not None:
            stmt = stmt.where(OrganizationActivityModel.organization_id == organization_id)

        if activity_ids is not None:
            stmt = stmt.where(OrganizationActivityModel.activity_id.in_(activity_ids))

        await self._session.execute(stmt)
        await self._session.flush()
