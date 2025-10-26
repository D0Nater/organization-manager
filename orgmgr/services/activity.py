"""Activity service."""

from collections.abc import Sequence
from typing import Any

from orgmgr.core.entities.activity import Activity
from orgmgr.core.exceptions.activity import ActivityNotFoundError
from orgmgr.core.interfaces.actions.activity import ActivityAction
from orgmgr.core.interfaces.queries.activity import ActivityQuery
from orgmgr.core.interfaces.repositories.activity import ActivityRepository
from orgmgr.core.types import ActivityId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class ActivityService:
    """Service layer for managing activity entities."""

    def __init__(
        self, activity_repository: ActivityRepository, activity_query: ActivityQuery, activity_action: ActivityAction
    ):
        """Initializes the ActivityService with a repository and an action handler for activity operations.

        Args:
            activity_repository (ActivityRepository): Repository for activity persistence.
            activity_query (ActivityQuery): Query for activity entities.
            activity_action (ActivityAction): Action handler containing domain-level activity validations.
        """
        self._activity_repository = activity_repository
        self._activity_query = activity_query
        self._activity_action = activity_action

    async def create(self, entity: Activity) -> Activity:
        """Creates a new activity entity after validating its parent existence and nesting constraints.

        Args:
            entity (Activity): The activity entity to be created.

        Returns:
            Activity: The newly created activity entity.

        Raises:
            ActivityNotFoundError: If the parent activity does not exist.
            ActivityMaximumNestingError: If the activity exceeds the allowed nesting depth.
        """
        if parent_id := entity.parent_id:
            await self.get_by_id(parent_id)
            await self._activity_action.validate_nesting(parent_id)

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
        return await self._activity_query.get_page(pagination, specifications, sort_specifications)

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
        """Updates an existing activity entity after validating parent existence and nesting depth.

        Args:
            entity (Activity): The activity entity containing updated attributes.

        Returns:
            Activity: The updated activity entity.

        Raises:
            ActivityNotFoundError: If the specified parent activity does not exist.
            ActivityMaximumNestingError: If the activity exceeds the allowed nesting depth.
        """
        if parent_id := entity.parent_id:
            await self.get_by_id(parent_id)
            await self._activity_action.validate_nesting(parent_id)

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
