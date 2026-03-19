"""Organization validator."""

from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.core.entities.organization import Organization
from orgmgr.core.exceptions.organization import OrganizationNotFoundError
from orgmgr.core.interfaces.repositories.organization import OrganizationRepository
from orgmgr.core.interfaces.validators.organization import OrganizationValidator
from orgmgr.core.types import OrganizationId
from orgmgr.lib.validators.sa_base import SABaseValidator
from orgmgr.models import OrganizationModel


class SAOrganizationValidator(SABaseValidator[Organization, OrganizationModel], OrganizationValidator):
    """SQLAlchemy validator implementation for organization."""

    model = OrganizationModel

    def __init__(self, session: AsyncSession, organization_repository: OrganizationRepository):
        """Initialize the organization validator.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
            organization_repository (OrganizationRepository): Repository used to access organization entities.
        """
        super().__init__(session)
        self._organization_repository = organization_repository

    async def ensure_exists(self, organization_id: OrganizationId) -> Organization:
        """Validate that a organization exists.

        Args:
            organization_id (OrganizationId): The unique identifier of the organization to validate.

        Returns:
            Organization: The organization entity that was validated.

        Raises:
            OrganizationNotFoundError: If no organization exists with the given ID.
        """
        organization = await self._organization_repository.get_by_id(organization_id)

        if organization is None:
            raise OrganizationNotFoundError(organization_id=organization_id)

        return organization
