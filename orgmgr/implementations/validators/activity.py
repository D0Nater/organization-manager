"""Activity validator."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.core.entities.activity import MAX_NESTING_LEVEL, Activity
from orgmgr.core.exceptions.activity import ActivityMaximumNestingError, ActivityNotFoundError
from orgmgr.core.interfaces.queries.activity import ActivityQuery
from orgmgr.core.interfaces.repositories.activity import ActivityRepository
from orgmgr.core.interfaces.validators.activity import ActivityValidator
from orgmgr.core.types import ActivityId
from orgmgr.lib.entities.page import PaginationInfo
from orgmgr.lib.specification.field import InListSpecification
from orgmgr.lib.validators.sa_base import SABaseValidator
from orgmgr.models import ActivityModel


class SAActivityValidator(SABaseValidator[Activity, ActivityModel], ActivityValidator):
    """SQLAlchemy validator implementation for activity."""

    model = ActivityModel

    def __init__(
        self,
        session: AsyncSession,
        activity_repository: ActivityRepository,
        activity_query: ActivityQuery,
    ):
        """Initialize the activity validator.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
            activity_repository (ActivityRepository): Repository used to access activity entities.
            activity_query (ActivityQuery): Query for activity entities.
        """
        super().__init__(session)
        self._activity_repository = activity_repository
        self._activity_query = activity_query

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

    async def ensure_exists_many(self, activity_ids: Sequence[ActivityId]) -> None:
        """Validates that all given activity IDs exist.

        Args:
            activity_ids (Sequence[ActivityId]): A sequence of unique activity identifiers to validate.

        Returns:
            None

        Raises:
            ActivityNotFoundError: If one or more activity IDs do not exist.
        """
        if not activity_ids:
            return

        spec = InListSpecification[Any]("id", activity_ids)
        existing_count = await self._activity_query.get_count([spec])
        if existing_count != len(activity_ids):
            found = await self._activity_query.get_list(
                pagination=PaginationInfo(page=1, per_page=None), specifications=[spec]
            )
            found_ids = {a.activity_id for a in found}
            missing = [str(aid) for aid in activity_ids if aid not in found_ids]
            raise ActivityNotFoundError(activity_id=missing)

    async def validate_nesting(self, parent_id: ActivityId) -> None:
        """Validates nesting depth by traversing the activity hierarchy until the maximum depth is reached.

        Args:
            parent_id (ActivityId): The unique identifier of the parent activity to validate.

        Returns:
            None

        Raises:
            ActivityNotFoundError: If the parent activity does not exist.
            ActivityMaximumNestingError: If the nesting depth equals or exceeds the defined MAX_NESTING_LEVEL.
        """
        depth = 1
        current = await self.ensure_exists(parent_id)

        while current.parent_id:
            depth += 1

            if depth >= MAX_NESTING_LEVEL:
                raise ActivityMaximumNestingError()

            current = await self.ensure_exists(current.parent_id)
