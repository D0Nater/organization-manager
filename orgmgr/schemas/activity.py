"""Activity schemas."""

from typing import Any, Self

from orgmgr.core.entities.activity import Activity
from orgmgr.core.types import ActivityId
from orgmgr.lib.schemas import fields as f
from orgmgr.lib.schemas.base import (
    BaseEntityCreateSchema,
    BaseEntitySchema,
    BaseEntityUpdateSchema,
    BaseFilterSchema,
    BaseSchema,
)
from orgmgr.lib.schemas.pagination import EntityPaginationResponse
from orgmgr.lib.specification.field import EqualsSpecification, ILikeSpecification, InListSpecification


ACTIVITY_ID = f.UUID(prefix="Activity ID.")
ACTIVITY_IDS = f.BaseField(description="Activity IDs.")
ACTIVITY_NAME = f.BaseField(description="Activity name.", max_length=128, exmples=["Food"])


class BaseActivitySchema(BaseSchema):
    """Base activity schema."""

    name: str = ACTIVITY_NAME
    parent_id: ActivityId | None = ACTIVITY_ID


class ActivitySchema(BaseActivitySchema, BaseEntitySchema[Activity]):
    """Activity schema."""

    id: ActivityId = ACTIVITY_ID

    @classmethod
    def from_entity(cls, entity: Activity) -> Self:
        """Convert a Activity domain entity into a ActivitySchema.

        Args:
            entity (Activity): The activity domain entity.

        Returns:
            Self: The corresponding schema instance.
        """
        return cls(
            id=entity.activity_id,
            parent_id=entity.parent_id,
            name=entity.name,
        )


class ActivityCreateSchema(BaseActivitySchema, BaseEntityCreateSchema[Activity]):
    """Activity create schema."""

    def to_entity(self, **kwargs: Any) -> Activity:
        """Convert the ActivityCreateSchema into a Activity domain entity.

        Returns:
            Activity: A new activity entity created from the schema data.
        """
        return Activity.create(**self.model_dump() | kwargs)


class ActivityUpdateSchema(BaseActivitySchema, BaseEntityUpdateSchema[Activity]):
    """Activity update schema."""


class ActivityPatchSchema(ActivityUpdateSchema):
    """Activity patch schema."""

    name: str = ACTIVITY_NAME(default=None)
    parent_id: ActivityId | None = ACTIVITY_ID(default=None)


class ActivityFilterSchema(BaseFilterSchema):
    """Activity filter schema."""

    ids: list[ActivityId] | None = ACTIVITY_IDS(default=None, specification=InListSpecification("id"))

    parent_id: ActivityId | None = ACTIVITY_ID(default=None, specification=EqualsSpecification("parent_id"))

    name_ilike: str | None = ACTIVITY_NAME(default=None, specification=ILikeSpecification("name"))


class ActivityPaginationSchema(EntityPaginationResponse[Activity, ActivitySchema]):
    """Activity pagination schema."""

    _item_schema = ActivitySchema
