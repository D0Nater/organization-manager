"""Organization Unit of Work."""

from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.core.interfaces.repositories.organization import OrganizationRepository
from orgmgr.core.interfaces.repositories.organization_activity import OrganizationActivityRepository
from orgmgr.core.interfaces.uow.organization import OrganizationUnitOfWork
from orgmgr.lib.uow.sa_base import SABaseUnitOfWork


class SAOrganizationUnitOfWork(SABaseUnitOfWork, OrganizationUnitOfWork):
    """SQLAlchemy Unit of Work implementation for organization service."""

    def __init__(
        self,
        session: AsyncSession,
        organization_repository: OrganizationRepository,
        organization_activity_repository: OrganizationActivityRepository,
    ) -> None:
        """Initialize the repository with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
            organization_repository (OrganizationRepository): Repository for organization persistence.
            organization_activity_repository (OrganizationActivityRepository): Repository for
                organization activity persistence.
        """
        super().__init__(session)
        self.organization_repository = organization_repository
        self.organization_activity_repository = organization_activity_repository
