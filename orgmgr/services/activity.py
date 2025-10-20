"""Activity service."""

from collections.abc import Sequence
from typing import Any

from orgmgr.core.entities.activity import Activity
from orgmgr.core.exceptions.activity import ActivityNotFoundError
from orgmgr.core.interfaces.repositories.activity import ActivityRepository
from orgmgr.core.types import ActivityId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class ActivityService:
    """Service layer for managing activity entities."""

    def __init__(self, activity_repository: ActivityRepository):
        """Initialize the activity service with a repository.

        Args:
            activity_repository (ActivityRepository): Repository for activity persistence.
        """
        self._activity_repository = activity_repository

    async def create(self, entity: Activity) -> Activity:
        """Create a new activity entity.

        Args:
            entity (Activity): The activity entity to create.

        Returns:
            Activity: The created activity entity.

        Raises:
            ActivityNotFoundError: If no parent activity exists with the given ID.
        """
        if entity.parent_id:
            await self.get_by_id(entity.parent_id)

        return await self._activity_repository.create(entity)

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
    ) -> Page[Activity]:
        """Retrieve a paginated list of activity entities matching optional specifications.

        Args:
            pagination (PaginationInfo): Pagination parameters including page number and items per page.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Optional filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Optional sort specifications.
                Defaults to None.

        Returns:
            Page[Activity]: Paginated items with total count and page metadata.
        """
        return await self._activity_repository.get_page(pagination, specifications, sort_specifications)

    async def get_by_id(self, activity_id: ActivityId) -> Activity:
        """Retrieve a single activity entity by its ID.

        Args:
            activity_id (ActivityId): The unique identifier of the activity to retrieve.

        Returns:
            Activity: The retrieved activity entity.

        Raises:
            ActivityNotFoundError: If no activity exists with the given ID.
        """
        activity = await self._activity_repository.get_by_id(activity_id)

        if activity is None:
            raise ActivityNotFoundError(activity_id=activity_id)

        return activity

    async def update(self, entity: Activity) -> Activity:
        """Update an existing activity entity.

        Args:
            entity (Activity): The activity entity with updated values.

        Returns:
            Activity: The updated activity entity.

        Raises:
            ActivityNotFoundError: If no parent activity exists with the given ID.
        """
        if entity.parent_id:
            await self.get_by_id(entity.parent_id)

        return await self._activity_repository.update(entity)

    async def delete(self, activity_id: ActivityId) -> None:
        """Delete a activity entity by its ID.

        Args:
            activity_id (ActivityId): The unique identifier of the activity to delete.

        Returns:
            None

        Raises:
            ActivityNotFoundError: If no activity exists with the given ID.
        """
        activity = await self.get_by_id(activity_id)
        await self._activity_repository.delete(activity.activity_id)
