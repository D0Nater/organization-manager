"""Repository provider."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.implementations.repositories import SAActivityRepository, SABuildingRepository
from orgmgr.implementations.repositories.organization import SAOrganizationRepository
from orgmgr.implementations.repositories.organization_activity import SAOrganizationActivityRepository


class RepositoryProvider(Provider):
    """Provider for repository instances."""

    @provide(scope=Scope.REQUEST)
    def activity_repository(self, db_session: AsyncSession) -> SAActivityRepository:
        """Provides a SQLAlchemy-based repository for activity entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SAActivityRepository: A repository instance for managing activity entities.
        """
        return SAActivityRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def building_repository(self, db_session: AsyncSession) -> SABuildingRepository:
        """Provides a SQLAlchemy-based repository for building entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SABuildingRepository: A repository instance for managing building entities.
        """
        return SABuildingRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def organization_repository(self, db_session: AsyncSession) -> SAOrganizationRepository:
        """Provides a SQLAlchemy-based repository for organization entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SAOrganizationRepository: A repository instance for managing organization entities.
        """
        return SAOrganizationRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def organization_activity_repository(self, db_session: AsyncSession) -> SAOrganizationActivityRepository:
        """Provides a SQLAlchemy-based repository for organization activity entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SAOrganizationActivityRepository: A repository instance for managing organization activity entities.
        """
        return SAOrganizationActivityRepository(db_session)
