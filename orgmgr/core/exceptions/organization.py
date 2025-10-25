"""Organization exceptions."""

from orgmgr.lib.exceptions.base import AbstractException, NotFoundException


class OrganizationError(AbstractException):
    """Base organization error."""


class OrganizationNotFoundError(OrganizationError, NotFoundException):
    """Organization not found."""

    auto_additional_info_fields = ["organization_id"]

    detail = "Organization {organization_id} not found"
