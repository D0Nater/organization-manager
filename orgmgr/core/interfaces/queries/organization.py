"""Organization query."""

from collections.abc import Sequence
from typing import Any, Protocol

from orgmgr.core.entities.organization import Organization
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.filters.base import BaseFilter
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class OrganizationQuery(Protocol):
    """Protocol defining the interface for organization queries."""

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseFilter[Any, Any]] | None = None,
    ) -> Page[Organization]:
        """Return a single page of organization entities that satisfy optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Sort specifications to apply.
                Defaults to None.
            filters (Sequence[BaseFilter[Any, Any]] | None): Filter to apply. Defaults to None.

        Returns:
            Page[Organization]: A page of organization entities with pagination metadata.
        """

    async def get_list(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseFilter[Any, Any]] | None = None,
    ) -> list[Organization]:
        """Retrieve a list of organization entities matching optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications.
                Defaults to None.
            filters (Sequence[BaseFilter[Any, Any]] | None): Filter to apply. Defaults to None.

        Returns:
            list[Organization]: A list of organization entities matching the given specifications.
        """

    async def get_count(
        self,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        filters: Sequence[BaseFilter[Any, Any]] | None = None,
    ) -> int:
        """Count the number of organization entities matching optional specifications.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications.
                Defaults to None.
            filters (Sequence[BaseFilter[Any, Any]] | None): Filter to apply. Defaults to None.

        Returns:
            int: The total count of organization entities matching the specifications.
        """
