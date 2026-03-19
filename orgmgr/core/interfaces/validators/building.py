"""Building validator interface."""

from typing import Protocol

from orgmgr.core.entities.building import Building
from orgmgr.core.types import BuildingId


class BuildingValidator(Protocol):
    """Protocol defining the interface for building validation."""

    async def ensure_exists(self, building_id: BuildingId) -> Building:
        """Ensure that a building exists.

        Args:
            building_id (BuildingId): The unique identifier of the building to validate.

        Returns:
            Building: The validated building entity.

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
        """
