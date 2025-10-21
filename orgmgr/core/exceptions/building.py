"""Building exceptions."""

from orgmgr.lib.exceptions.base import AbstractException, NotFoundException


class BuildingError(AbstractException):
    """Base building error."""


class BuildingNotFoundError(BuildingError, NotFoundException):
    """Building not found."""

    auto_additional_info_fields = ["building_id"]

    detail = "Building {building_id} not found"
