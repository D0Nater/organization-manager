"""Base SQLAlchemy repository."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.filters.sa_base import BaseSQLAlchemyFilter
from orgmgr.lib.models import BaseModel
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification
from orgmgr.lib.specification.sqlalchemy import (
    add_filters_to_query,
    add_sort_specifications_to_query,
    add_specifications_to_query,
)
from orgmgr.lib.utils.pagination import add_pagination_to_query


class SABaseRepository[ID, E, M: BaseModel[Any]]:
    """Generic SQLAlchemy base repository for managing CRUD operations on models.

    This repository provides common methods for creating, retrieving, updating, soft-deleting, and restoring entities.
    It uses SQLAlchemy's AsyncSession and requires that the model extends AbstractModel with proper entity conversion.
    """

    model: type[M]
    pk_name: str = "id"

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        """
        self._session = session

    async def create(self, entity: E) -> E:
        """Create a new entity in the database and return it.

        Args:
            entity (E): The entity object to persist.

        Returns:
            E: The persisted entity with updated state (e.g., primary key).
        """
        model = self.model.from_entity(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> Page[E]:
        """Return a single page of entities that satisfy optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Sort specifications to apply.
                Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

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
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> list[E]:
        """Retrieve a list of entities matching optional specifications and sorting.

        Args:
            pagination (PaginationInfo): Pagination parameters.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of specifications. Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications. Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

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
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> int:
        """Count the number of rows matching optional specifications.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of specifications. Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

        Returns:
            int: The total count of matching rows.
        """
        stmt = select(func.count()).select_from(self.model)
        stmt = self.build_list_stmt(specifications, filters=filters, base_stmt=stmt)
        return (await self._session.execute(stmt)).scalar_one()

    async def get_by_id(self, entity_id: ID) -> E | None:
        """Retrieve a single entity by its primary key.

        Args:
            entity_id (ID): The primary key value of the entity to retrieve.

        Returns:
            E | None: The entity if found, otherwise None.
        """
        stmt = select(self.model).where(getattr(self.model, self.pk_name) == entity_id)
        res = await self._session.execute(stmt)
        m = res.scalar_one_or_none()
        return m.to_entity() if m else None

    async def update(self, entity: E) -> E:
        """Update an existing entity in the database and return it.

        Args:
            entity (E): The entity object with updated data.

        Returns:
            E: The updated entity.
        """
        model = self.model.from_entity(entity)
        await self._session.merge(model)
        await self._session.flush()
        return model.to_entity()

    async def delete(self, entity_id: ID) -> None:
        """Delete a single entity by its primary key.

        Args:
            entity_id (ID): The primary key value of the entity to delete.

        Returns:
            None
        """
        stmt = delete(self.model).where(getattr(self.model, self.pk_name) == entity_id)
        await self._session.execute(stmt)

    def build_list_stmt(
        self,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
        base_stmt: Select[Any] | None = None,
    ) -> Select[Any]:
        """Build a SQLAlchemy select statement for retrieving entities with optional filters and sorting.

        Args:
            specifications (Sequence[FieldSpecification[Any, Any]] | None): A list of filter specifications to apply.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): A list of sort specifications to apply.
                Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.
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
