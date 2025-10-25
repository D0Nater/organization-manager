"""Building repository."""

from collections.abc import Sequence
from typing import Any, Protocol

from orgmgr.core.entities.building import Building
from orgmgr.core.types import BuildingId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class BuildingRepository(Protocol):
    """Protocol defining the interface for building repositories."""

    async def create(self, building: Building) -> Building:
        """Create a new building entity.

        Args:
            building (Building): The building entity to create.

        Returns:
            Building: The created building entity.
        """

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
    ) -> Page[Building]:
        """Return a single page of building entities that satisfy optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Sort specifications to apply.
                Defaults to None.

        Returns:
            Page[Building]: A page of building entities with pagination metadata.
        """

    async def get_list(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
    ) -> list[Building]:
        """Retrieve a list of building entities matching optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications.
                Defaults to None.

        Returns:
            list[Building]: A list of building entities matching the given specifications.
        """

    async def get_count(self, specifications: Sequence[FieldSpecification[Any, Any]] | None = None) -> int:
        """Count the number of building entities matching optional specifications.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.

        Returns:
            int: The total count of building entities matching the specifications.
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
