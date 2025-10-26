"""Building repository."""

from typing import Protocol

from orgmgr.core.entities.building import Building
from orgmgr.core.types import BuildingId


class BuildingRepository(Protocol):
    """Protocol defining the interface for building repositories."""

    async def create(self, building: Building) -> Building:
        """Create a new building entity.

        Args:
            building (Building): The building entity to create.

        Returns:
            Building: The created building entity.
        """

    async def get_by_id(self, building_id: BuildingId) -> Building | None:
        """Retrieve a single building entity by its ID.

        Args:
            building_id (BuildingId): The unique identifier of the building to retrieve.

        Returns:
            Building | None: The retrieved building entity, or None if not found.
        """

    async def update(self, building: Building) -> Building:
        """Update an existing building entity.

        Args:
            building (Building): The building entity with updated values.

        Returns:
            Building: The updated building entity.
        """

    async def delete(self, building_id: BuildingId) -> None:
        """Delete an existing building entity by its ID.

        Args:
            building_id (BuildingId): The unique identifier of the building to delete.

        Returns:
            None
        """
