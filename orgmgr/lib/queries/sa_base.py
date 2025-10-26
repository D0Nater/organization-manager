"""Base SQLAlchemy query."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.filters.base import BaseFilter
from orgmgr.lib.models import BaseModel
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification
from orgmgr.lib.specification.sqlalchemy import (
    add_filters_to_query,
    add_sort_specifications_to_query,
    add_specifications_to_query,
)
from orgmgr.lib.utils.pagination import add_pagination_to_query


class SABaseQuery[E, M: BaseModel[Any]]:
    """Generic SQLAlchemy base query for managing CRUD operations on models.

    This query provides common methods for retrieving entities.
    It uses SQLAlchemy's AsyncSession and requires that the model extends AbstractModel with proper entity conversion.
    """

    model: type[M]

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the query with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        """
        self._session = session

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseFilter[Any, Select[Any]]] | None = None,
    ) -> Page[E]:
        """Return a single page of entities that satisfy optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Sort specifications to apply.
                Defaults to None.
            filters (Sequence[BaseFilter[Any, Select[Any]]] | None): Filter to apply. Defaults to None.

        Returns:
            Page[E]: A page of entities with pagination metadata.
        """
        items = await self.get_list(pagination, specifications, sort_specifications, filters)
        total = await self.get_count(specifications, filters)
        return Page(items=items, total=total, page=pagination.page, per_page=pagination.per_page)

    async def get_list(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseFilter[Any, Select[Any]]] | None = None,
    ) -> list[E]:
        """Retrieve a list of entities matching optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of specifications. Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications. Defaults to None.
            filters (Sequence[BaseFilter[Any, Select[Any]]] | None): Filter to apply. Defaults to None.

        Returns:
            list[E]: A list of entities matching the given specifications.
        """
        stmt = self.build_list_stmt(specifications, sort_specifications, filters)
        if pagination.per_page:
            stmt = add_pagination_to_query(stmt, limit=pagination.per_page, page=pagination.page)
        res = await self._session.execute(stmt)
        return [m.to_entity() for m in res.scalars().all()]

    async def get_count(
        self,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        filters: Sequence[BaseFilter[Any, Select[Any]]] | None = None,
    ) -> int:
        """Count the number of rows matching optional specifications.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of specifications. Defaults to None.
            filters (Sequence[BaseFilter[Any, Select[Any]]] | None): Filter to apply. Defaults to None.

        Returns:
            int: The total count of matching rows.
        """
        stmt = select(func.count()).select_from(self.model)
        stmt = self.build_list_stmt(specifications, filters=filters, base_stmt=stmt)
        return (await self._session.execute(stmt)).scalar_one()

    def build_list_stmt(
        self,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseFilter[Any, Select[Any]]] | None = None,
        base_stmt: Select[Any] | None = None,
    ) -> Select[Any]:
        """Build a SQLAlchemy select statement for retrieving entities with optional filters and sorting.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications to apply.
                Defaults to None.
            filters (Sequence[BaseFilter[Any, Select[Any]]] | None): Filter to apply. Defaults to None.
            base_stmt (Select[Any] | None): An optional base SQLAlchemy select statement. Defaults to None.

        Returns:
            Select[Any]: A SQLAlchemy select statement with applied filters and sorting.
        """
        stmt = select(self.model) if base_stmt is None else base_stmt

        if specifications:
            stmt = add_specifications_to_query(stmt, self.model, specifications)
        if sort_specifications:
            stmt = add_sort_specifications_to_query(stmt, self.model, sort_specifications)
        if filters:
            stmt = add_filters_to_query(stmt, filters)

        return stmt
