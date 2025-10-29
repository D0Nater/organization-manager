"""Unit of Work provider."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.implementations.repositories.organization import SAOrganizationRepository
from orgmgr.implementations.repositories.organization_activity import SAOrganizationActivityRepository
from orgmgr.implementations.uow.organization import SAOrganizationUnitOfWork


class UnitOfWorkProvider(Provider):
    """Provider for Unit of Work instances."""

    @provide(scope=Scope.REQUEST)
    def organization_uow(
        self,
        db_session: AsyncSession,
        organization_repository: SAOrganizationRepository,
        organization_activity_repository: SAOrganizationActivityRepository,
    ) -> SAOrganizationUnitOfWork:
        """Provides a SQLAlchemy-based Unit of Work.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.
            organization_repository (SAOrganizationRepository): Repository instance for organization entities.
            organization_activity_repository (SAOrganizationActivityRepository): Repository instance
                for organization activity entities.

        Returns:
            SAOrganizationUnitOfWork: A Unit of Work instance.
        """
        return SAOrganizationUnitOfWork(
            db_session,
            organization_repository,
            organization_activity_repository,
        )
