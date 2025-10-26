"""SQLAlchemy organization query."""

from orgmgr.core.entities.organization import Organization
from orgmgr.core.interfaces.queries.organization import OrganizationQuery
from orgmgr.lib.queries.sa_base import SABaseQuery
from orgmgr.models import OrganizationModel


class SAOrganizationQuery(SABaseQuery[Organization, OrganizationModel], OrganizationQuery):
    """SQLAlchemy query implementation for retrieving organization entities."""

    model = OrganizationModel
