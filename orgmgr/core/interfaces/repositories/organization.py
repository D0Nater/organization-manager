"""Organization repository."""

from collections.abc import Sequence
from typing import Any, Protocol

from orgmgr.core.entities.organization import Organization
from orgmgr.core.types import OrganizationId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.filters.sa_base import BaseSQLAlchemyFilter
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class OrganizationRepository(Protocol):
    """Protocol defining the interface for organization repositories."""

    async def create(self, organization: Organization) -> Organization:
        """Create a new organization entity.

        Args:
            organization (Organization): The organization entity to create.

        Returns:
            Organization: The created organization entity.
        """

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> Page[Organization]:
        """Return a single page of organization entities that satisfy optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Sort specifications to apply.
                Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

        Returns:
            Page[Organization]: A page of organization entities with pagination metadata.
        """

    async def get_list(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> list[Organization]:
        """Retrieve a list of organization entities matching optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications.
                Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

        Returns:
            list[Organization]: A list of organization entities matching the given specifications.
        """

    async def get_count(
        self,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> int:
        """Count the number of organization entities matching optional specifications.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

        Returns:
            int: The total count of organization entities matching the specifications.
        """

    async def get_by_id(self, organization_id: OrganizationId) -> Organization | None:
        """Retrieve a single organization entity by its ID.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to retrieve.

        Returns:
            Organization | None: The retrieved organization entity, or None if not found.
        """

    async def update(self, organization: Organization) -> Organization:
        """Update an existing organization entity.

        Args:
            organization (Organization): The organization entity with updated values.

        Returns:
            Organization: The updated organization entity.
        """

    async def delete(self, organization_id: OrganizationId) -> None:
        """Delete an existing organization entity by its ID.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to delete.

        Returns:
            None
        """
