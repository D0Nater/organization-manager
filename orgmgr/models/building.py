"""Building model."""

from typing import TYPE_CHECKING, Self
from uuid import uuid4

from sqlalchemy import Float, String, Uuid as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orgmgr.core.entities.building import Building
from orgmgr.core.types import BuildingId
from orgmgr.lib.entities.coordinate import Coordinate
from orgmgr.lib.models import BaseModel


if TYPE_CHECKING:
    from orgmgr.models import OrganizationModel


class BuildingModel(BaseModel[Building]):
    """SQLAlchemy model representing the building table."""

    __tablename__ = "buildings"

    id: Mapped[BuildingId] = mapped_column("id", SqlUUID(), primary_key=True, default=uuid4)
    """Building ID."""

    address: Mapped[str] = mapped_column("address", String(), nullable=False)
    """Building address."""

    latitude: Mapped[float] = mapped_column("latitude", Float(), nullable=False)
    """Building latitude."""

    longitude: Mapped[float] = mapped_column("longitude", Float(), nullable=False)
    """Building longitude."""

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        "OrganizationModel", back_populates="building", cascade="all, delete-orphan"
    )

    @classmethod
    def from_entity(cls, entity: Building) -> Self:
        """Convert a Building domain entity into a BuildingModel instance.

        Args:
            entity (Building): The building domain entity.

        Returns:
            Self: The corresponding SQLAlchemy model instance.
        """
        return cls(
            id=entity.building_id,
            address=entity.address,
            latitude=entity.coordinate.latitude,
            longitude=entity.coordinate.longitude,
        )

    def to_entity(self) -> Building:
        """Convert the BuildingModel instance into a Building domain entity.

        Returns:
            Building: The corresponding domain entity.
        """
        return Building(
            building_id=self.id,
            address=self.address,
            coordinate=Coordinate(self.latitude, self.longitude),
        )
