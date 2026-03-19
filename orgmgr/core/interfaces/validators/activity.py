"""Activity validator interface."""

from typing import Protocol

from orgmgr.core.entities.activity import Activity
from orgmgr.core.types import ActivityId


class ActivityValidator(Protocol):
    """Protocol defining the interface for activity validation."""

    async def ensure_exists(self, activity_id: ActivityId) -> Activity:
        """Ensure that a activity exists.

        Args:
            activity_id (ActivityId): The unique identifier of the activity to validate.

        Returns:
            Activity: The validated activity entity.

        Raises:
            ActivityNotFoundError: If no activity exists with the given ID.
        """

    async def validate_nesting(self, parent_id: ActivityId) -> None:
        """Validates whether a new activity can be nested under the specified parent without exceeding max depth.

        Args:
            parent_id (ActivityId): The unique identifier of the parent activity to validate.

        Returns:
            None

        Raises:
            ActivityMaximumNestingError: If adding a new activity under
                the specified parent exceeds the maximum nesting level.
        """
