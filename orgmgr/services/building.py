"""Building service."""

from collections.abc import Sequence
from typing import Any

from orgmgr.core.entities.building import Building
from orgmgr.core.exceptions.building import BuildingNotFoundError
from orgmgr.core.interfaces.queries.building import BuildingQuery
from orgmgr.core.interfaces.repositories.building import BuildingRepository
from orgmgr.core.types import BuildingId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class BuildingService:
    """Service layer for managing building entities."""

    def __init__(self, building_repository: BuildingRepository, building_query: BuildingQuery):
        """Initializes the BuildingService with a repository and an action handler for building operations.

        Args:
            building_repository (BuildingRepository): Repository for building persistence.
            building_query (BuildingQuery): Query for building entities.
        """
        self._building_repository = building_repository
        self._building_query = building_query

    async def create(self, entity: Building) -> Building:
        """Creates a new building entity after validating its parent existence and nesting constraints.

        Args:
            entity (Building): The building entity to be created.

        Returns:
            Building: The newly created building entity.
        """
        return await self._building_repository.create(entity)

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
    ) -> Page[Building]:
        """Retrieve a paginated list of building entities matching optional specifications.

        Args:
            pagination (PaginationInfo): Pagination parameters including page number and items per page.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Optional filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Optional sort specifications.
                Defaults to None.

        Returns:
            Page[Building]: Paginated items with total count and page metadata.
        """
        return await self._building_query.get_page(pagination, specifications, sort_specifications)

    async def get_by_id(self, building_id: BuildingId) -> Building:
        """Retrieve a single building entity by its ID.

        Args:
            building_id (BuildingId): The unique identifier of the building to retrieve.

        Returns:
            Building: The retrieved building entity.

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
        """
        building = await self._building_repository.get_by_id(building_id)

        if building is None:
            raise BuildingNotFoundError(building_id=building_id)

        return building

    async def update(self, entity: Building) -> Building:
        """Updates an existing building entity after validating parent existence and nesting depth.

        Args:
            entity (Building): The building entity containing updated attributes.

        Returns:
            Building: The updated building entity.
        """
        return await self._building_repository.update(entity)

    async def delete(self, building_id: BuildingId) -> None:
        """Delete a building entity by its ID.

        Args:
            building_id (BuildingId): The unique identifier of the building to delete.

        Returns:
            None

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
        """
        building = await self.get_by_id(building_id)
        await self._building_repository.delete(building.building_id)
