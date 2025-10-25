"""Activity endpoints."""

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from pyfa_converter_v2 import QueryDepends

from orgmgr.core.exceptions.activity import ActivityMaximumNestingError, ActivityNotFoundError
from orgmgr.core.types import ActivityId
from orgmgr.dependencies.auth import require_auth
from orgmgr.lib.entities.page import PaginationInfo
from orgmgr.lib.schemas.pagination import PaginationRequest
from orgmgr.lib.utils.openapi import exc_list
from orgmgr.schemas.activity import (
    ActivityCreateSchema,
    ActivityFilterSchema,
    ActivityPaginationSchema,
    ActivityPatchSchema,
    ActivitySchema,
    ActivityUpdateSchema,
)
from orgmgr.services import ActivityService


router = APIRouter(
    tags=["activities"],
    prefix="/activities",
    route_class=DishkaRoute,
    dependencies=[Depends(require_auth())],
)


@router.post(
    "/",
    status_code=201,
    response_model=ActivitySchema,
    openapi_extra=exc_list(ActivityNotFoundError, ActivityMaximumNestingError),
)
async def create_activity(
    activity_service: FromDishka[ActivityService],
    schema: ActivityCreateSchema,
) -> ActivitySchema:
    """Create a new activity."""
    entity = schema.to_entity()
    created_entity = await activity_service.create(entity)
    return ActivitySchema.from_entity(created_entity)


@router.get("/", response_model=ActivityPaginationSchema)
async def get_activities(
    activity_service: FromDishka[ActivityService],
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: ActivityFilterSchema = QueryDepends(ActivityFilterSchema),
) -> ActivityPaginationSchema:
    """Retrieve a paginated list of activity."""
    pagination_info = PaginationInfo(page=pagination.page, per_page=pagination.limit)
    page = await activity_service.get_page(
        pagination_info,
        specifications=filters.to_field_specifications(),
        sort_specifications=filters.to_sort_specifications(),
    )
    return ActivityPaginationSchema.from_page(page)


@router.get(
    "/{activity_id}",
    response_model=ActivitySchema,
    openapi_extra=exc_list(ActivityNotFoundError),
)
async def get_activity(
    activity_service: FromDishka[ActivityService],
    activity_id: ActivityId,
) -> ActivitySchema:
    """Retrieve a single activity by its ID."""
    entity = await activity_service.get_by_id(activity_id)
    return ActivitySchema.from_entity(entity)


@router.put(
    "/{activity_id}",
    response_model=ActivitySchema,
    openapi_extra=exc_list(ActivityNotFoundError, ActivityMaximumNestingError),
)
async def update_activity(
    activity_service: FromDishka[ActivityService],
    activity_id: ActivityId,
    schema: ActivityUpdateSchema,
) -> ActivitySchema:
    """Update an existing activity with new values."""
    entity = await activity_service.get_by_id(activity_id)
    updated_entity = schema.update_entity(entity)
    saved_entity = await activity_service.update(updated_entity)
    return ActivitySchema.from_entity(saved_entity)


@router.patch(
    "/{activity_id}",
    response_model=ActivitySchema,
    openapi_extra=exc_list(ActivityNotFoundError, ActivityMaximumNestingError),
)
async def patch_activity(
    activity_service: FromDishka[ActivityService],
    activity_id: ActivityId,
    schema: ActivityPatchSchema,
) -> ActivitySchema:
    """Apply partial updates to an existing activity."""
    entity = await activity_service.get_by_id(activity_id)
    updated_entity = schema.update_entity(entity)
    saved_entity = await activity_service.update(updated_entity)
    return ActivitySchema.from_entity(saved_entity)


@router.delete(
    "/{activity_id}",
    status_code=204,
    openapi_extra=exc_list(ActivityNotFoundError),
)
async def delete_activity(
    activity_service: FromDishka[ActivityService],
    activity_id: ActivityId,
) -> None:
    """Delete an activity by its ID."""
    return await activity_service.delete(activity_id)
