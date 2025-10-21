"""Captcha config repository."""

from collections.abc import Sequence
from typing import Any, Protocol

from orgmgr.core.entities.activity import Activity
from orgmgr.core.types import ActivityId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class ActivityRepository(Protocol):
    """Protocol defining the interface for activity repositories."""

    async def create(self, activity: Activity) -> Activity:
        """Create a new activity entity.

        Args:
            activity (Activity): The activity entity to create.

        Returns:
            Activity: The created activity entity.
        """

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
    ) -> Page[Activity]:
        """Return a single page of activity entities that satisfy optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Sort specifications to apply.
                Defaults to None.

        Returns:
            Page[Activity]: A page of activity entities with pagination metadata.
        """

    async def get_list(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
    ) -> list[Activity]:
        """Retrieve a list of activity entities matching optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications.
                Defaults to None.

        Returns:
            list[Activity]: A list of activity entities matching the given specifications.
        """

    async def get_count(self, specifications: Sequence[FieldSpecification[Any, Any]] | None = None) -> int:
        """Count the number of activity entities matching optional specifications.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.

        Returns:
            int: The total count of activity entities matching the specifications.
        """

    async def get_by_id(self, activity_id: ActivityId) -> Activity | None:
        """Retrieve a single activity entity by its ID.

        Args:
            activity_id (ActivityId): The unique identifier of the activity to retrieve.

        Returns:
            Activity | None: The retrieved activity entity, or None if not found.
        """

    async def update(self, activity: Activity) -> Activity:
        """Update an existing activity entity.

        Args:
            activity (Activity): The activity entity with updated values.

        Returns:
            Activity: The updated activity entity.
        """

    async def delete(self, activity_id: ActivityId) -> None:
        """Delete an existing activity entity by its ID.

        Args:
            activity_id (ActivityId): The unique identifier of the activity to delete.

        Returns:
            None
        """
