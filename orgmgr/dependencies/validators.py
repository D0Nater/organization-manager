"""Validator provider."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.implementations.queries import SAActivityQuery
from orgmgr.implementations.repositories import SAActivityRepository, SABuildingRepository, SAOrganizationRepository
from orgmgr.implementations.validators import SAActivityValidator, SABuildingValidator, SAOrganizationValidator


class ValidatorProvider(Provider):
    """Provider for validator instances."""

    @provide(scope=Scope.REQUEST)
    def activity_validator(
        self,
        db_session: AsyncSession,
        activity_repository: SAActivityRepository,
        activity_query: SAActivityQuery,
    ) -> SAActivityValidator:
        """Provides a validator for activity entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.
            activity_repository (SAActivityRepository): Repository used to retrieve activity entities.
            activity_query (SAActivityQuery): Query instance for activity entities.

        Returns:
            SAActivityValidator: An implementation of SAActivityValidator based on SQLAlchemy.
        """
        return SAActivityValidator(db_session, activity_repository, activity_query)

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

    @provide(scope=Scope.REQUEST)
    def organization_validator(
        self, db_session: AsyncSession, organization_repository: SAOrganizationRepository
    ) -> SAOrganizationValidator:
        """Provides a validator for organization entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.
            organization_repository (SAOrganizationRepository): Repository used to retrieve organization entities.

        Returns:
            SAOrganizationValidator: An implementation of SAOrganizationValidator based on SQLAlchemy.
        """
        return SAOrganizationValidator(db_session, organization_repository)
