"""Building schemas."""

from collections.abc import Sequence
from typing import Any, Self

from orgmgr.core.entities.building import Building
from orgmgr.core.types import BuildingId
from orgmgr.lib.entities.coordinate import Coordinate
from orgmgr.lib.schemas import fields as f
from orgmgr.lib.schemas.base import (
    BaseEntityCreateSchema,
    BaseEntitySchema,
    BaseEntityUpdateSchema,
    BaseFilterSchema,
    BaseSchema,
)
from orgmgr.lib.schemas.pagination import EntityPaginationResponse
from orgmgr.lib.specification.field import (
    GreaterThanOrEqualsToSpecification,
    ILikeSpecification,
    InListSpecification,
    LessThanOrEqualsToSpecification,
)


BUILDING_ID = f.UUID(prefix="Building ID.")
BUILDING_IDS = f.BaseField(description="Building IDs.")
BUILDING_ADDRESS = f.BaseField(description="Building address.")
BUILDING_LATITUDE = f.BaseField(description="Building latitude.")
BUILDING_LONGITUDE = f.BaseField(description="Building longitude.")


class BaseBuildingSchema(BaseSchema):
    """Base building schema."""

    address: str = BUILDING_ADDRESS
    latitude: float = BUILDING_LATITUDE
    longitude: float = BUILDING_LONGITUDE


class BuildingSchema(BaseBuildingSchema, BaseEntitySchema[Building]):
    """Building schema."""

    id: BuildingId = BUILDING_ID

    @classmethod
    def from_entity(cls, entity: Building) -> Self:
        """Convert a Building domain entity into a BuildingSchema.

        Args:
            entity (Building): The building domain entity.

        Returns:
            Self: The corresponding schema instance.
        """
        return cls(
            id=entity.building_id,
            address=entity.address,
            latitude=entity.coordinate.latitude,
            longitude=entity.coordinate.longitude,
        )


class BuildingCreateSchema(BaseBuildingSchema, BaseEntityCreateSchema[Building]):
    """Building create schema."""

    def to_entity(self, **kwargs: Any) -> Building:
        """Convert the BuildingCreateSchema into a Building domain entity.

        Returns:
            Building: A new building entity created from the schema data.
        """
        coordinate = Coordinate(self.latitude, self.longitude)
        return Building.create(coordinate=coordinate, **self.model_dump(exclude={"latitude", "longitude"}) | kwargs)


class BuildingUpdateSchema(BaseBuildingSchema, BaseEntityUpdateSchema[Building]):
    """Building update schema."""

    def update_entity(self, entity: Building, exclude: Sequence[str] | None = None) -> Building:
        """Update the given entity with fields set in the schema.

        Args:
            entity (Building): The entity instance to update.
            exclude (Sequence[str] | None): Optional list of field names to exclude from update. Defaults to None.

        Returns:
            Building: The updated entity with fields modified according to the schema.
        """
        if self.latitude or self.longitude:
            latitude = self.latitude or entity.coordinate.latitude
            longitude = self.longitude or entity.coordinate.longitude
            entity.coordinate = Coordinate(latitude, longitude)

        return super().update_entity(entity, exclude=list(exclude or []) + ["latitude", "longitude"])


class BuildingPatchSchema(BuildingUpdateSchema):
    """Building patch schema."""

    address: str = BUILDING_ADDRESS(default=None)
    latitude: float = BUILDING_LATITUDE(default=None)
    longitude: float = BUILDING_LONGITUDE(default=None)


class BuildingFilterSchema(BaseFilterSchema):
    """Building filter schema."""

    ids: list[BuildingId] | None = BUILDING_IDS(default=None, specification=InListSpecification("id"))

    address_ilike: str | None = BUILDING_ADDRESS(default=None, specification=ILikeSpecification("address"))

    latitude_ge: float | None = BUILDING_LATITUDE(
        default=None, specification=GreaterThanOrEqualsToSpecification("latitude")
    )
    latitude_le: float | None = BUILDING_LATITUDE(
        default=None, specification=LessThanOrEqualsToSpecification("latitude")
    )

    longitude_ge: float | None = BUILDING_LATITUDE(
        default=None, specification=GreaterThanOrEqualsToSpecification("longitude")
    )
    longitude_le: float | None = BUILDING_LATITUDE(
        default=None, specification=LessThanOrEqualsToSpecification("longitude")
    )


class BuildingPaginationSchema(EntityPaginationResponse[Building, BuildingSchema]):
    """Building pagination schema."""

    _item_schema = BuildingSchema
