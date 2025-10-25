"""Organization activity model."""

from typing import Self
from uuid import UUID

from sqlalchemy import ForeignKey, Uuid as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column

from orgmgr.core.entities.organization_activity import OrganizationActivity
from orgmgr.lib.models import BaseModel


class OrganizationActivityModel(BaseModel[OrganizationActivity]):
    """SQLAlchemy-модель для связи Organization ↔ Activity."""

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
        """Преобразует доменную сущность в SQLAlchemy-модель."""
        return cls(
            organization_id=entity.organization_id,
            activity_id=entity.activity_id,
        )

    def to_entity(self) -> OrganizationActivity:
        """Преобразует SQLAlchemy-модель в доменную сущность."""
        return OrganizationActivity(
            organization_id=self.organization_id,
            activity_id=self.activity_id,
        )
