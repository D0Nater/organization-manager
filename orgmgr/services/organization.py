"""Organization service."""

from collections.abc import Sequence
from typing import Any

from orgmgr.core.entities.organization import Organization
from orgmgr.core.interfaces.queries.organization import OrganizationQuery
from orgmgr.core.interfaces.uow.organization import OrganizationUnitOfWork
from orgmgr.core.interfaces.validators.activity import ActivityValidator
from orgmgr.core.interfaces.validators.building import BuildingValidator
from orgmgr.core.interfaces.validators.organization import OrganizationValidator
from orgmgr.core.types import OrganizationId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.filters.base import BaseFilter
from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


class OrganizationService:
    """Service layer for managing organization entities."""

    def __init__(
        self,
        organization_uow: OrganizationUnitOfWork,
        organization_query: OrganizationQuery,
        organization_validator: OrganizationValidator,
        building_validator: BuildingValidator,
        activity_validator: ActivityValidator,
    ):
        """Initialize the organization service.

        Args:
            organization_uow (OrganizationUnitOfWork): Organization Unit of Work.
            organization_query (OrganizationQuery): Query for organization entities.
            organization_validator (OrganizationValidator): Validator ensuring organization existence.
            building_validator (BuildingValidator): Validator ensuring building existence.
            activity_validator (ActivityValidator): Validator ensuring activity existence.
        """
        self._organization_uow = organization_uow
        self._organization_query = organization_query
        self._organization_validator = organization_validator
        self._building_validator = building_validator
        self._activity_validator = activity_validator

    async def create(self, entity: Organization) -> Organization:
        """Creates a new organization entity after validating its parent existence and nesting constraints.

        Args:
            entity (Organization): The organization entity to be created.

        Returns:
            Organization: The newly created organization entity.

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
            ActivityNotFoundError: If one or more activity IDs do not exist.
        """
        activity_ids = entity.activity_ids

        await self._building_validator.ensure_exists(entity.building_id)
        await self._activity_validator.ensure_exists_many(activity_ids)

        async with self._organization_uow:
            created = await self._organization_uow.organization_repository.create(entity)
            created.activity_ids = activity_ids

            if activity_ids:
                await self._organization_uow.organization_activity_repository.create(
                    created.organization_id, activity_ids
                )

        return created

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseFilter[Any, Any]] | None = None,
    ) -> Page[Organization]:
        """Retrieve a paginated list of organization entities matching optional specifications.

        Args:
            pagination (PaginationInfo): Pagination parameters including page number and items per page.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Optional filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Optional sort specifications.
                Defaults to None.
            filters (Sequence[BaseFilter[Any, Any]] | None): Filter to apply. Defaults to None.

        Returns:
            Page[Organization]: Paginated items with total count and page metadata.
        """
        return await self._organization_query.get_page(pagination, specifications, sort_specifications, filters)

    async def get_by_id(self, organization_id: OrganizationId) -> Organization:
        """Retrieve a single organization entity by its ID.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to retrieve.

        Returns:
            Organization: The retrieved organization entity.

        Raises:
            OrganizationNotFoundError: If no organization exists with the given ID.
        """
        return await self._organization_validator.ensure_exists(organization_id)

    async def update(self, entity: Organization) -> Organization:
        """Updates an existing organization entity after validating parent existence and nesting depth.

        Args:
            entity (Organization): The organization entity containing updated attributes.

        Returns:
            Organization: The updated organization entity.

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
            ActivityNotFoundError: If one or more activity IDs do not exist.
        """
        activity_ids = entity.activity_ids

        await self._building_validator.ensure_exists(entity.building_id)
        await self._activity_validator.ensure_exists_many(activity_ids)

        async with self._organization_uow:
            saved = await self._organization_uow.organization_repository.update(entity)
            saved.activity_ids = activity_ids

            await self._organization_uow.organization_activity_repository.delete(organization_id=saved.organization_id)
            if activity_ids:
                await self._organization_uow.organization_activity_repository.create(
                    saved.organization_id, activity_ids
                )

        return saved

    async def delete(self, organization_id: OrganizationId) -> None:
        """Delete a organization entity by its ID.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to delete.

        Returns:
            None

        Raises:
            OrganizationNotFoundError: If no organization exists with the given ID.
        """
        organization = await self._organization_validator.ensure_exists(organization_id)

        async with self._organization_uow:
            await self._organization_uow.organization_activity_repository.delete(organization_id=organization_id)
            await self._organization_uow.organization_repository.delete(organization.organization_id)
