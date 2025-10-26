"""Activity repository."""

from typing import Protocol

from orgmgr.core.entities.activity import Activity
from orgmgr.core.types import ActivityId


class ActivityRepository(Protocol):
    """Protocol defining the interface for activity repositories."""

    async def create(self, activity: Activity) -> Activity:
        """Create a new activity entity.

        Args:
            activity (Activity): The activity entity to create.

        Returns:
            Activity: The created activity entity.
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
