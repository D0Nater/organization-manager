"""Activity action."""

from orgmgr.core.entities.activity import MAX_NESTING_LEVEL
from orgmgr.core.exceptions.activity import ActivityMaximumNestingError
from orgmgr.core.interfaces.actions.activity import ActivityAction
from orgmgr.core.interfaces.repositories.activity import ActivityRepository
from orgmgr.core.types import ActivityId


class SAActivityAction(ActivityAction):
    """Implements activity domain actions using SQLAlchemy repositories."""

    def __init__(self, activity_repository: ActivityRepository):
        """Initializes the activity action implementation with the provided repository.

        Args:
            activity_repository (ActivityRepository): Repository used for retrieving activity hierarchy data.
        """
        self._repo = activity_repository

    async def validate_nesting(self, parent_id: ActivityId) -> None:
        """Validates nesting depth by traversing the activity hierarchy until the maximum depth is reached.

        Args:
            parent_id (ActivityId): The unique identifier of the parent activity to validate.

        Returns:
            None

        Raises:
            ActivityMaximumNestingError: If the nesting depth equals or exceeds the defined MAX_NESTING_LEVEL.
        """
        depth = 1
        current = await self._repo.get_by_id(parent_id)
        while current and current.parent_id:
            depth += 1
            if depth >= MAX_NESTING_LEVEL:
                raise ActivityMaximumNestingError()
            current = await self._repo.get_by_id(current.parent_id)
