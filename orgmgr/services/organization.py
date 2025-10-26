"""Organization service."""

from collections.abc import Sequence
from typing import Any

from orgmgr.core.entities.organization import Organization
from orgmgr.core.exceptions.activity import ActivityNotFoundError
from orgmgr.core.exceptions.building import BuildingNotFoundError
from orgmgr.core.exceptions.organization import OrganizationNotFoundError
from orgmgr.core.interfaces.queries.activity import ActivityQuery
from orgmgr.core.interfaces.queries.organization import OrganizationQuery
from orgmgr.core.interfaces.repositories.building import BuildingRepository
from orgmgr.core.interfaces.repositories.organization import OrganizationRepository
from orgmgr.core.interfaces.repositories.organization_activity import OrganizationActivityRepository
from orgmgr.core.types import ActivityId, BuildingId, OrganizationId
from orgmgr.lib.entities.page import Page, PaginationInfo
from orgmgr.lib.filters.sa_base import BaseSQLAlchemyFilter
from orgmgr.lib.specification.field import FieldSpecification, InListSpecification
from orgmgr.lib.specification.sort import SortSpecification


class OrganizationService:
    """Service layer for managing organization entities."""

    def __init__(
        self,
        organization_repository: OrganizationRepository,
        organization_query: OrganizationQuery,
        building_repository: BuildingRepository,
        activity_query: ActivityQuery,
        organization_activity_repository: OrganizationActivityRepository,
    ):
        """Initializes the OrganizationService with a repository and an action handler for organization operations.

        Args:
            organization_repository (OrganizationRepository): Repository for organization persistence.
            organization_query (OrganizationQuery): Query for organization entities.
            building_repository (BuildingRepository): Repository for building persistence.
            activity_query (ActivityQuery): Query for activity entities.
            organization_activity_repository (OrganizationActivityRepository): Repository for
                organization activity persistence.
        """
        self._organization_repository = organization_repository
        self._organization_query = organization_query
        self._building_repository = building_repository
        self._activity_query = activity_query
        self._organization_activity_repository = organization_activity_repository

    async def create(self, entity: Organization) -> Organization:
        """Creates a new organization entity after validating its parent existence and nesting constraints.

        Args:
            entity (Organization): The organization entity to be created.

        Returns:
            Organization: The newly created organization entity.
        """
        activity_ids = entity.activity_ids

        await self._validate_building_exists(entity.building_id)
        await self._validate_activities_exist(activity_ids)

        created = await self._organization_repository.create(entity)
        created.activity_ids = activity_ids

        if activity_ids:
            await self._organization_activity_repository.create(created.organization_id, activity_ids)

        return created

    async def get_page(
        self,
        pagination: PaginationInfo,
        specifications: Sequence[FieldSpecification[Any, Any]] | None = None,
        sort_specifications: Sequence[SortSpecification] | None = None,
        filters: Sequence[BaseSQLAlchemyFilter[Any]] | None = None,
    ) -> Page[Organization]:
        """Retrieve a paginated list of organization entities matching optional specifications.

        Args:
            pagination (PaginationInfo): Pagination parameters including page number and items per page.
            specifications (Sequence[FieldSpecification[Any, Any]] | None): Optional filter specifications.
                Defaults to None.
            sort_specifications (Sequence[SortSpecification] | None): Optional sort specifications.
                Defaults to None.
            filters (Sequence[BaseSQLAlchemyFilter[Any]] | None): Filter to apply. Defaults to None.

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
        organization = await self._organization_repository.get_by_id(organization_id)

        if organization is None:
            raise OrganizationNotFoundError(organization_id=organization_id)

        return organization

    async def update(self, entity: Organization) -> Organization:
        """Updates an existing organization entity after validating parent existence and nesting depth.

        Args:
            entity (Organization): The organization entity containing updated attributes.

        Returns:
            Organization: The updated organization entity.
        """
        activity_ids = entity.activity_ids

        await self._validate_building_exists(entity.building_id)
        await self._validate_activities_exist(activity_ids)

        saved = await self._organization_repository.update(entity)
        saved.activity_ids = activity_ids

        if activity_ids:
            await self._organization_activity_repository.delete(organization_id=saved.organization_id)
            if activity_ids:
                await self._organization_activity_repository.create(saved.organization_id, activity_ids)

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
        organization = await self.get_by_id(organization_id)
        await self._organization_activity_repository.delete(organization_id=organization_id)
        await self._organization_repository.delete(organization.organization_id)

    async def _validate_building_exists(self, building_id: BuildingId) -> None:
        """Validates that a building with the given ID exists.

        Args:
            building_id (BuildingId): The unique identifier of the building to validate.

        Returns:
            None

        Raises:
            BuildingNotFoundError: If no building exists with the given ID.
        """
        building = await self._building_repository.get_by_id(building_id)
        if building is None:
            raise BuildingNotFoundError(building_id=building_id)

    async def _validate_activities_exist(self, activity_ids: Sequence[ActivityId] | None) -> None:
        """Validates that all given activity IDs exist.

        Args:
            activity_ids (Sequence[ActivityId] | None): A sequence of unique activity identifiers to validate.

        Returns:
            None

        Raises:
            ActivityNotFoundError: If one or more activity IDs do not exist.
        """
        if not activity_ids:
            return

        spec = InListSpecification[Any]("id", activity_ids)
        existing_count = await self._activity_query.get_count([spec])
        if existing_count != len(activity_ids):
            found = await self._activity_query.get_list(
                pagination=PaginationInfo(page=1, per_page=None), specifications=[spec]
            )
            found_ids = {a.activity_id for a in found}
            missing = [aid for aid in activity_ids if aid not in found_ids]
            raise ActivityNotFoundError(activity_id=missing)
