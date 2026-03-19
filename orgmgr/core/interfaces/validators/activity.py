"""Activity validator interface."""

from collections.abc import Sequence
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

    async def ensure_exists_many(self, activity_ids: Sequence[ActivityId]) -> None:
        """Validates that all given activity IDs exist.

        Args:
            activity_ids (Sequence[ActivityId]): A sequence of unique activity identifiers to validate.

        Returns:
            None

        Raises:
            ActivityNotFoundError: If one or more activity IDs do not exist.
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
