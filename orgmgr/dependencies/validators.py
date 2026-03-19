"""Validator provider."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.implementations.repositories import SAActivityRepository
from orgmgr.implementations.validators import SAActivityValidator


class ValidatorProvider(Provider):
    """Provider for validator instances."""

    @provide(scope=Scope.REQUEST)
    def activity_validator(
        self, db_session: AsyncSession, activity_repository: SAActivityRepository
    ) -> SAActivityValidator:
        """Provides a validator for activity entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.
            activity_repository (SAActivityRepository): Repository used to retrieve activity entities.

        Returns:
            SAActivityValidator: An implementation of SAActivityValidator based on SQLAlchemy.
        """
        return SAActivityValidator(db_session, activity_repository)
