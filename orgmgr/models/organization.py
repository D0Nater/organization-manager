"""Organization model."""

from typing import TYPE_CHECKING, Self
from uuid import uuid4

from sqlalchemy import ForeignKey, String, Uuid as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orgmgr.core.entities.organization import Organization
from orgmgr.core.types import BuildingId, OrganizationId
from orgmgr.lib.entities.phone_number import PhoneNumber
from orgmgr.lib.models import BaseModel
from orgmgr.lib.sqlalchemy_types.phone_number import PhoneNumberType


if TYPE_CHECKING:
    from orgmgr.models import ActivityModel, BuildingModel


class OrganizationModel(BaseModel[Organization]):
    """SQLAlchemy model representing the organization table."""

    __tablename__ = "organizations"

    id: Mapped[OrganizationId] = mapped_column("id", SqlUUID(), primary_key=True, default=uuid4)
    """Organization ID."""

    building_id: Mapped[BuildingId] = mapped_column(
        "building_id", SqlUUID(), ForeignKey("buildings.id", ondelete="RESTRICT"), nullable=False
    )
    """The ID of the building where the organization is located."""

    name: Mapped[str] = mapped_column("name", String(255), nullable=False)
    """The name of the organization."""

    phone_numbers: Mapped[list[PhoneNumber]] = mapped_column("phone_numbers", PhoneNumberType(), nullable=False)
    """The organization's phone numbers."""

    building: Mapped[list["BuildingModel"]] = relationship("BuildingModel", back_populates="organizations")
    activities: Mapped[list["ActivityModel"]] = relationship(
        "ActivityModel", secondary="organization_activities", backref="organizations", lazy="selectin"
    )

    @classmethod
    def from_entity(cls, entity: Organization) -> Self:
        """Convert a Organization domain entity into a OrganizationModel instance.

        Args:
            entity (Organization): The organization domain entity.

        Returns:
            Self: The corresponding SQLAlchemy model instance.
        """
        return cls(
            id=entity.organization_id,
            name=entity.name,
            phone_numbers=entity.phone_numbers,
            building_id=entity.building_id,
        )

    def to_entity(self) -> Organization:
        """Convert the OrganizationModel instance into a Organization domain entity.

        Returns:
            Organization: The corresponding domain entity.
        """
        return Organization(
            organization_id=self.id,
            name=self.name,
            phone_numbers=self.phone_numbers,
            building_id=self.building_id,
            activity_ids=[a.id for a in self.activities] if self.activities else [],
        )
