"""Organization Unit of Work."""

from orgmgr.core.interfaces.repositories.organization import OrganizationRepository
from orgmgr.core.interfaces.repositories.organization_activity import OrganizationActivityRepository
from orgmgr.lib.uow.base import BaseUnitOfWork


class OrganizationUnitOfWork(BaseUnitOfWork):
    """Organization Unit of Work."""

    organization_repository: OrganizationRepository
    organization_activity_repository: OrganizationActivityRepository
