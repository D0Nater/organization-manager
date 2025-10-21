"""SQLAlchemy building repository."""

from orgmgr.core.entities.building import Building
from orgmgr.core.interfaces.repositories.building import BuildingRepository
from orgmgr.core.types import BuildingId
from orgmgr.lib.repositories.sa_base import SABaseRepository
from orgmgr.models import BuildingModel


class SABuildingRepository(SABaseRepository[BuildingId, Building, BuildingModel], BuildingRepository):
    """SQLAlchemy repository implementation for managing building entities."""

    model = BuildingModel
