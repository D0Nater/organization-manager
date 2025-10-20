"""Activity exceptions."""

from orgmgr.lib.exceptions.base import AbstractException, NotFoundException


class ActivityError(AbstractException):
    """Base activity error."""


class ActivityNotFoundError(ActivityError, NotFoundException):
    """Activity not found."""

    auto_additional_info_fields = ["activity_id"]

    detail = "Activity {activity_id} not found"
