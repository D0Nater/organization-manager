"""SQLAlchemy activity repository."""

from orgmgr.core.entities.activity import Activity
from orgmgr.core.interfaces.repositories.activity import ActivityRepository
from orgmgr.core.types import ActivityId
from orgmgr.lib.repositories.sa_base import SABaseRepository
from orgmgr.models import ActivityModel


class SAActivityRepository(SABaseRepository[ActivityId, Activity, ActivityModel], ActivityRepository):
    """SQLAlchemy repository implementation for managing activity entities."""

    model = ActivityModel
