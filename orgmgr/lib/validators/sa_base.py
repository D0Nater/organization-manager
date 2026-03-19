"""Base SQLAlchemy validator."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.lib.models import BaseModel


class SABaseValidator[E, M: BaseModel[Any]]:
    """Generic SQLAlchemy validator for models.

    Provides reusable validation logic using AsyncSession.
    Works with SQLAlchemy models extending BaseModel.
    """

    model: type[M]

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the validator with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        """
        self._session = session
