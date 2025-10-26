"""Organization activity model."""

from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey, Uuid as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column

from orgmgr.core.entities.organization_activity import OrganizationActivity
from orgmgr.lib.models import BaseModel


class OrganizationActivityModel(BaseModel[OrganizationActivity]):
    """SQLAlchemy is a model for communication Organization - Activity."""

    __tablename__ = "organization_activities"

    organization_id: Mapped[UUID] = mapped_column(
        "organization_id", SqlUUID(), ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True
    )
    """Organization ID."""

    activity_id: Mapped[UUID] = mapped_column(
        "activity_id", SqlUUID(), ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    """Activity ID."""

    @classmethod
    def from_entity(cls, entity: OrganizationActivity) -> Self:
        """Convert a OrganizationActivity domain entity into a OrganizationActivityModel instance.

        Args:
            entity (OrganizationActivity): The organization activity domain entity.

        Returns:
            Self: The corresponding SQLAlchemy model instance.
        """
        return cls(
            organization_id=entity.organization_id,
            activity_id=entity.activity_id,
        )

    def to_entity(self) -> OrganizationActivity:
        """Convert the OrganizationActivityModel instance into a OrganizationActivity domain entity.

        Returns:
            OrganizationActivity: The corresponding domain entity.
        """
        return OrganizationActivity(
            organization_id=self.organization_id,
            activity_id=self.activity_id,
        )
