"""Activity action."""

from typing import Protocol

from orgmgr.core.types import ActivityId


class ActivityAction(Protocol):
    """Activity action."""

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
