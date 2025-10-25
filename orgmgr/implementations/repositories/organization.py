"""SQLAlchemy organization repository."""

from orgmgr.core.entities.organization import Organization
from orgmgr.core.interfaces.repositories.organization import OrganizationRepository
from orgmgr.core.types import OrganizationId
from orgmgr.lib.repositories.sa_base import SABaseRepository
from orgmgr.models import OrganizationModel


class SAOrganizationRepository(
    SABaseRepository[OrganizationId, Organization, OrganizationModel], OrganizationRepository
):
    """SQLAlchemy repository implementation for managing organization entities."""

    model = OrganizationModel
