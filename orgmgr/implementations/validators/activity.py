"""Activity validator."""

from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.core.entities.activity import MAX_NESTING_LEVEL, Activity
from orgmgr.core.exceptions.activity import ActivityMaximumNestingError, ActivityNotFoundError
from orgmgr.core.interfaces.repositories.activity import ActivityRepository
from orgmgr.core.interfaces.validators.activity import ActivityValidator
from orgmgr.core.types import ActivityId
from orgmgr.lib.validators.sa_base import SABaseValidator
from orgmgr.models import ActivityModel


class SAActivityValidator(SABaseValidator[Activity, ActivityModel], ActivityValidator):
    """SQLAlchemy validator implementation for activity."""

    model = ActivityModel

    def __init__(self, session: AsyncSession, activity_repository: ActivityRepository):
        """Initialize the activity validator.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
            activity_repository (ActivityRepository): Repository used to access activity entities.
        """
        super().__init__(session)
        self._activity_repository = activity_repository

    async def ensure_exists(self, activity_id: ActivityId) -> Activity:
        """Validate that a activity exists.

        Args:
            activity_id (ActivityId): The unique identifier of the activity to validate.

        Returns:
            Activity: The activity entity that was validated.

        Raises:
            ActivityNotFoundError: If no activity exists with the given ID.
        """
        activity = await self._activity_repository.get_by_id(activity_id)

        if activity is None:
            raise ActivityNotFoundError(activity_id=activity_id)

        return activity

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
        current = await self.ensure_exists(parent_id)

        while current.parent_id:
            depth += 1

            if depth >= MAX_NESTING_LEVEL:
                raise ActivityMaximumNestingError()

            current = await self.ensure_exists(current.parent_id)
