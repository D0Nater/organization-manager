"""SQLAlchemy activity query."""

from orgmgr.core.entities.activity import Activity
from orgmgr.core.interfaces.queries.activity import ActivityQuery
from orgmgr.lib.queries.sa_base import SABaseQuery
from orgmgr.models import ActivityModel


class SAActivityQuery(SABaseQuery[Activity, ActivityModel], ActivityQuery):
    """SQLAlchemy query implementation for retrieving activity entities."""

    model = ActivityModel
