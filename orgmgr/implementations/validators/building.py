"""Building validator."""

from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.core.entities.building import Building
from orgmgr.core.exceptions.building import BuildingNotFoundError
from orgmgr.core.interfaces.repositories.building import BuildingRepository
from orgmgr.core.interfaces.validators.building import BuildingValidator
from orgmgr.core.types import BuildingId
from orgmgr.lib.validators.sa_base import SABaseValidator
from orgmgr.models import BuildingModel


class SABuildingValidator(SABaseValidator[Building, BuildingModel], BuildingValidator):
    """SQLAlchemy validator implementation for building."""

    model = BuildingModel

    def __init__(self, session: AsyncSession, building_repository: BuildingRepository):
        """Initialize the building validator.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
            building_repository (BuildingRepository): Repository used to access building entities.
        """
        super().__init__(session)
        self._building_repository = building_repository

    async def ensure_exists(self, building_id: BuildingId) -> Building:
        """Validate that a building exists.

        Args:
            building_id (BuildingId): The unique identifier of the building to validate.

        Returns:
            Building: The building entity that was validated.

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
        """
        building = await self._building_repository.get_by_id(building_id)

        if building is None:
            raise BuildingNotFoundError(building_id=building_id)

        return building
