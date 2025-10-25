"""Organization endpoints."""

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from pyfa_converter_v2 import QueryDepends

from orgmgr.core.exceptions.activity import ActivityNotFoundError
from orgmgr.core.exceptions.building import BuildingNotFoundError
from orgmgr.core.exceptions.organization import OrganizationNotFoundError
from orgmgr.core.types import OrganizationId
from orgmgr.lib.entities.page import PaginationInfo
from orgmgr.lib.schemas.pagination import PaginationRequest
from orgmgr.lib.utils.openapi import exc_list
from orgmgr.schemas.organization import (
    OrganizationCreateSchema,
    OrganizationFilterSchema,
    OrganizationPaginationSchema,
    OrganizationPatchSchema,
    OrganizationSchema,
    OrganizationUpdateSchema,
)
from orgmgr.services import OrganizationService


router = APIRouter(tags=["organizations"], prefix="/organizations", route_class=DishkaRoute)


@router.post(
    "/",
    status_code=201,
    response_model=OrganizationSchema,
    openapi_extra=exc_list(ActivityNotFoundError, BuildingNotFoundError),
)
async def create_organization(
    organization_service: FromDishka[OrganizationService],
    schema: OrganizationCreateSchema,
) -> OrganizationSchema:
    """Create a new organization."""
    entity = schema.to_entity()
    created_entity = await organization_service.create(entity)
    return OrganizationSchema.from_entity(created_entity)


@router.get("/", response_model=OrganizationPaginationSchema)
async def get_organizations(
    organization_service: FromDishka[OrganizationService],
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: OrganizationFilterSchema = QueryDepends(OrganizationFilterSchema),
) -> OrganizationPaginationSchema:
    """Retrieve a paginated list of organization."""
    pagination_info = PaginationInfo(page=pagination.page, per_page=pagination.limit)
    page = await organization_service.get_page(
        pagination_info,
        specifications=filters.to_field_specifications(),
        sort_specifications=filters.to_sort_specifications(),
        filters=filters.to_filters(),
    )
    return OrganizationPaginationSchema.from_page(page)


@router.get(
    "/{organization_id}",
    response_model=OrganizationSchema,
    openapi_extra=exc_list(OrganizationNotFoundError),
)
async def get_organization(
    organization_service: FromDishka[OrganizationService],
    organization_id: OrganizationId,
) -> OrganizationSchema:
    """Retrieve a single organization by its ID."""
    entity = await organization_service.get_by_id(organization_id)
    return OrganizationSchema.from_entity(entity)


@router.put(
    "/{organization_id}",
    response_model=OrganizationSchema,
    openapi_extra=exc_list(OrganizationNotFoundError, ActivityNotFoundError, BuildingNotFoundError),
)
async def update_organization(
    organization_service: FromDishka[OrganizationService],
    organization_id: OrganizationId,
    schema: OrganizationUpdateSchema,
) -> OrganizationSchema:
    """Update an existing organization with new values."""
    entity = await organization_service.get_by_id(organization_id)
    updated_entity = schema.update_entity(entity)
    saved_entity = await organization_service.update(updated_entity)
    return OrganizationSchema.from_entity(saved_entity)


@router.patch(
    "/{organization_id}",
    response_model=OrganizationSchema,
    openapi_extra=exc_list(OrganizationNotFoundError, ActivityNotFoundError, BuildingNotFoundError),
)
async def patch_organization(
    organization_service: FromDishka[OrganizationService],
    organization_id: OrganizationId,
    schema: OrganizationPatchSchema,
) -> OrganizationSchema:
    """Apply partial updates to an existing organization."""
    entity = await organization_service.get_by_id(organization_id)
    updated_entity = schema.update_entity(entity)
    saved_entity = await organization_service.update(updated_entity)
    return OrganizationSchema.from_entity(saved_entity)


@router.delete(
    "/{organization_id}",
    status_code=204,
    openapi_extra=exc_list(OrganizationNotFoundError),
)
async def delete_organization(
    organization_service: FromDishka[OrganizationService],
    organization_id: OrganizationId,
) -> None:
    """Delete an organization by its ID."""
    return await organization_service.delete(organization_id)
