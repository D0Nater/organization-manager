"""Validator provider."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.implementations.repositories import SAActivityRepository
from orgmgr.implementations.repositories.building import SABuildingRepository
from orgmgr.implementations.validators import SAActivityValidator
from orgmgr.implementations.validators.building import SABuildingValidator


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

    @provide(scope=Scope.REQUEST)
    def building_validator(
        self, db_session: AsyncSession, building_repository: SABuildingRepository
    ) -> SABuildingValidator:
        """Provides a validator for building entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.
            building_repository (SABuildingRepository): Repository used to retrieve building entities.

        Returns:
            SABuildingValidator: An implementation of SABuildingValidator based on SQLAlchemy.
        """
        return SABuildingValidator(db_session, building_repository)
