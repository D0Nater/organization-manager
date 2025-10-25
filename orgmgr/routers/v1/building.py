"""Building endpoints."""

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from pyfa_converter_v2 import QueryDepends

from orgmgr.core.exceptions.building import BuildingNotFoundError
from orgmgr.core.types import BuildingId
from orgmgr.dependencies.auth import require_auth
from orgmgr.lib.entities.page import PaginationInfo
from orgmgr.lib.schemas.pagination import PaginationRequest
from orgmgr.lib.utils.openapi import exc_list
from orgmgr.schemas.building import (
    BuildingCreateSchema,
    BuildingFilterSchema,
    BuildingPaginationSchema,
    BuildingPatchSchema,
    BuildingSchema,
    BuildingUpdateSchema,
)
from orgmgr.services import BuildingService


router = APIRouter(
    tags=["buildings"],
    prefix="/buildings",
    route_class=DishkaRoute,
    dependencies=[Depends(require_auth())],
)


@router.post("/", status_code=201, response_model=BuildingSchema)
async def create_building(
    building_service: FromDishka[BuildingService],
    schema: BuildingCreateSchema,
) -> BuildingSchema:
    """Create a new building."""
    entity = schema.to_entity()
    created_entity = await building_service.create(entity)
    return BuildingSchema.from_entity(created_entity)


@router.get("/", response_model=BuildingPaginationSchema)
async def get_buildings(
    building_service: FromDishka[BuildingService],
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: BuildingFilterSchema = QueryDepends(BuildingFilterSchema),
) -> BuildingPaginationSchema:
    """Retrieve a paginated list of building."""
    pagination_info = PaginationInfo(page=pagination.page, per_page=pagination.limit)
    page = await building_service.get_page(
        pagination_info,
        specifications=filters.to_field_specifications(),
        sort_specifications=filters.to_sort_specifications(),
    )
    return BuildingPaginationSchema.from_page(page)


@router.get(
    "/{building_id}",
    response_model=BuildingSchema,
    openapi_extra=exc_list(BuildingNotFoundError),
)
async def get_building(
    building_service: FromDishka[BuildingService],
    building_id: BuildingId,
) -> BuildingSchema:
    """Retrieve a single building by its ID."""
    entity = await building_service.get_by_id(building_id)
    return BuildingSchema.from_entity(entity)


@router.put(
    "/{building_id}",
    response_model=BuildingSchema,
    openapi_extra=exc_list(BuildingNotFoundError),
)
async def update_building(
    building_service: FromDishka[BuildingService],
    building_id: BuildingId,
    schema: BuildingUpdateSchema,
) -> BuildingSchema:
    """Update an existing building with new values."""
    entity = await building_service.get_by_id(building_id)
    updated_entity = schema.update_entity(entity)
    saved_entity = await building_service.update(updated_entity)
    return BuildingSchema.from_entity(saved_entity)


@router.patch(
    "/{building_id}",
    response_model=BuildingSchema,
    openapi_extra=exc_list(BuildingNotFoundError),
)
async def patch_building(
    building_service: FromDishka[BuildingService],
    building_id: BuildingId,
    schema: BuildingPatchSchema,
) -> BuildingSchema:
    """Apply partial updates to an existing building."""
    entity = await building_service.get_by_id(building_id)
    updated_entity = schema.update_entity(entity)
    saved_entity = await building_service.update(updated_entity)
    return BuildingSchema.from_entity(saved_entity)


@router.delete(
    "/{building_id}",
    status_code=204,
    openapi_extra=exc_list(BuildingNotFoundError),
)
async def delete_building(
    building_service: FromDishka[BuildingService],
    building_id: BuildingId,
) -> None:
    """Delete an building by its ID."""
    return await building_service.delete(building_id)
