"""Activity exceptions."""

from orgmgr.lib.exceptions.base import AbstractException, ConflictException, NotFoundException


class ActivityError(AbstractException):
    """Base activity error."""


class ActivityNotFoundError(ActivityError, NotFoundException):
    """Activity not found."""

    auto_additional_info_fields = ["activity_id"]

    detail = "Activity {activity_id} not found"


class ActivityMaximumNestingError(ActivityError, ConflictException):
    """Activity maximum nesting error."""

    detail = "Activity maximum nesting error"
