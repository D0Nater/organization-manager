"""SQLAlchemy building query."""

from orgmgr.core.entities.building import Building
from orgmgr.core.interfaces.queries.building import BuildingQuery
from orgmgr.lib.queries.sa_base import SABaseQuery
from orgmgr.models import BuildingModel


class SABuildingQuery(SABaseQuery[Building, BuildingModel], BuildingQuery):
    """SQLAlchemy query implementation for retrieving building entities."""

    model = BuildingModel
