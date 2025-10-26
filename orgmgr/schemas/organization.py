"""Organization schemas."""

from collections.abc import Sequence
from typing import Annotated, Any, Self

from orgmgr.core.entities.organization import Organization
from orgmgr.core.types import ActivityId, BuildingId, OrganizationId
from orgmgr.filters.organization import ActivityIdInListFilter, ActivityIdInListWithChildrenFilter, CoordinateFilter
from orgmgr.lib.entities.phone_number import PhoneNumber
from orgmgr.lib.schemas import fields as f, validators as v
from orgmgr.lib.schemas.base import (
    BaseEntityCreateSchema,
    BaseEntitySchema,
    BaseEntityUpdateSchema,
    BaseFilterSchema,
    BaseSchema,
)
from orgmgr.lib.schemas.pagination import EntityPaginationResponse
from orgmgr.lib.specification.field import ILikeSpecification, InListSpecification
from orgmgr.schemas.activity import ACTIVITY_IDS
from orgmgr.schemas.building import BUILDING_ID, BUILDING_IDS


ORGANIZATION_ID = f.UUID(description="Organization ID.")
ORGANIZATION_IDS = f.BaseField(description="Organization IDs.")
ORGANIZATION_NAME = f.BaseField(description="Organization name.", max_length=255, examples=["ООО 'Ромашка'"])
ORGANIZATION_PHONES = f.BaseField(description="Organization phone numbers.", examples=[["+79998887766"]])

CoordFilterStr = Annotated[
    str, v.python_regex(r"^-?\d+(\.\d+)?,[\s]?-?\d+(\.\d+)?;[\s]?-?\d+(\.\d+)?,[\s]?-?\d+(\.\d+)?$")
]


class BaseOrganizationSchema(BaseSchema):
    """Base organization schema."""

    name: str = ORGANIZATION_NAME
    phone_numbers: list[str] = ORGANIZATION_PHONES
    building_id: BuildingId = BUILDING_ID
    activity_ids: list[ActivityId] = ACTIVITY_IDS


class OrganizationSchema(BaseOrganizationSchema, BaseEntitySchema[Organization]):
    """Organization schema."""

    id: OrganizationId = ORGANIZATION_ID

    @classmethod
    def from_entity(cls, entity: Organization) -> Self:
        """Convert a Organization domain entity into a OrganizationSchema.

        Args:
            entity (Organization): The organization domain entity.

        Returns:
            Self: The corresponding schema instance.
        """
        return cls(
            id=entity.organization_id,
            name=entity.name,
            phone_numbers=[i.number for i in entity.phone_numbers],
            building_id=entity.building_id,
            activity_ids=entity.activity_ids,
        )


class OrganizationCreateSchema(BaseOrganizationSchema, BaseEntityCreateSchema[Organization]):
    """Organization create schema."""

    def to_entity(self, **kwargs: Any) -> Organization:
        """Convert the OrganizationCreateSchema into a Organization domain entity.

        Returns:
            Organization: A new organization entity created from the schema data.
        """
        phone_numbers = list(map(PhoneNumber, self.phone_numbers))
        return Organization.create(phone_numbers=phone_numbers, **self.model_dump(exclude={"phone_numbers"}) | kwargs)


class OrganizationUpdateSchema(BaseOrganizationSchema, BaseEntityUpdateSchema[Organization]):
    """Organization update schema."""

    def update_entity(self, entity: Organization, exclude: Sequence[str] | None = None) -> Organization:
        """Update the given entity with fields set in the schema.

        Args:
            entity (Organization): The entity instance to update.
            exclude (Sequence[str] | None): Optional list of field names to exclude from update. Defaults to None.

        Returns:
            Organization: The updated entity with fields modified according to the schema.
        """
        if "phone_numbers" in self.model_fields_set:
            entity.phone_numbers = list(map(PhoneNumber, self.phone_numbers))

        return super().update_entity(entity, exclude=list(exclude or []) + ["phone_numbers"])


class OrganizationPatchSchema(OrganizationUpdateSchema):
    """Organization patch schema."""

    name: str = ORGANIZATION_NAME(default=None)
    phone_numbers: list[str] = ORGANIZATION_PHONES(default=None)
    building_id: BuildingId = BUILDING_ID(default=None)
    activity_ids: list[ActivityId] = ACTIVITY_IDS(default=None)


class OrganizationFilterSchema(BaseFilterSchema):
    """Organization filter schema."""

    ids: list[OrganizationId] | None = ORGANIZATION_IDS(default=None, specification=InListSpecification("id"))

    building_ids: list[BuildingId] | None = BUILDING_IDS(default=None, specification=InListSpecification("building_id"))

    activity_ids: list[ActivityId] | None = ACTIVITY_IDS(default=None, filter=ActivityIdInListFilter)

    activity_ids_with_children: list[ActivityId] | None = ACTIVITY_IDS(
        default=None, filter=ActivityIdInListWithChildrenFilter
    )

    coords: CoordFilterStr | None = f.BaseField(
        description="Coordinates like 55.759961,37.637420;55.756001,37.647054", default=None, filter=CoordinateFilter
    )

    name_ilike: str | None = ORGANIZATION_NAME(default=None, specification=ILikeSpecification("name"))


class OrganizationPaginationSchema(EntityPaginationResponse[Organization, OrganizationSchema]):
    """Organization pagination schema."""

    _item_schema = OrganizationSchema
