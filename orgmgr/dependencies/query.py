"""Query provider."""

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.implementations.queries import SAActivityQuery, SABuildingQuery, SAOrganizationQuery


class QueryProvider(Provider):
    """Provider for query instances."""

    @provide(scope=Scope.REQUEST)
    def activity_query(self, db_session: AsyncSession) -> SAActivityQuery:
        """Provides a SQLAlchemy-based query for activity entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SAActivityQuery: A query instance for managing activity entities.
        """
        return SAActivityQuery(db_session)

    @provide(scope=Scope.REQUEST)
    def building_query(self, db_session: AsyncSession) -> SABuildingQuery:
        """Provides a SQLAlchemy-based query for building entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SABuildingQuery: A query instance for managing building entities.
        """
        return SABuildingQuery(db_session)

    @provide(scope=Scope.REQUEST)
    def organization_query(self, db_session: AsyncSession) -> SAOrganizationQuery:
        """Provides a SQLAlchemy-based query for organization entities.

        Args:
            db_session (AsyncSession): The SQLAlchemy asynchronous session for database operations.

        Returns:
            SAOrganizationQuery: A query instance for managing organization entities.
        """
        return SAOrganizationQuery(db_session)
