"""Activity model."""

from typing import Self
from uuid import uuid4

from sqlalchemy import ForeignKey, String, Uuid as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column

from orgmgr.core.entities.activity import Activity
from orgmgr.core.types import ActivityId
from orgmgr.lib.models import BaseModel


class ActivityModel(BaseModel[Activity]):
    """SQLAlchemy model representing the captcha configuration table."""

    __tablename__ = "activities"

    id: Mapped[ActivityId] = mapped_column("id", SqlUUID(), primary_key=True, default=uuid4)
    """Activity ID."""

    parent_id: Mapped[ActivityId | None] = mapped_column(
        "parent_id", SqlUUID(), ForeignKey("activities.id", ondelete="CASCADE"), nullable=True
    )
    """Activity parent ID."""

    name: Mapped[str] = mapped_column("name", String(128), nullable=False)
    """Activity name."""

    @classmethod
    def from_entity(cls, entity: Activity) -> Self:
        """Convert a Activity domain entity into a ActivityModel instance.

        Args:
            entity (Activity): The captcha config domain entity.

        Returns:
            Self: The corresponding SQLAlchemy model instance.
        """
        return cls(
            id=entity.activity_id,
            parent_id=entity.parent_id,
            name=entity.name,
        )

    def to_entity(self) -> Activity:
        """Convert the ActivityModel instance into a Activity domain entity.

        Returns:
            Activity: The corresponding domain entity.
        """
        return Activity(
            activity_id=self.id,
            parent_id=self.parent_id,
            name=self.name,
        )
