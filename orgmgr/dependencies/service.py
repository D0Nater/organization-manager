"""Service provider."""

from dishka import Scope, provide
from dishka.integrations.fastapi import FastapiProvider

from orgmgr.implementations.actions import SAActivityAction
from orgmgr.implementations.repositories import (
    SAActivityRepository,
    SABuildingRepository,
    SAOrganizationActivityRepository,
    SAOrganizationRepository,
)
from orgmgr.services import ActivityService, BuildingService, OrganizationService


class ServiceProvider(FastapiProvider):
    """Provider for service layer instances."""

    @provide(scope=Scope.REQUEST)
    def activity_service(
        self, activity_repository: SAActivityRepository, activity_action: SAActivityAction
    ) -> ActivityService:
        """Provides the ActivityService for managing activities.

        Args:
            activity_repository (SAActivityRepository): Repository instance for activity entities.
            activity_action (SAActivityAction): Action instance for activity entities.

        Returns:
            ActivityService: A service instance for handling activity logic.
        """
        return ActivityService(activity_repository, activity_action)

    @provide(scope=Scope.REQUEST)
    def building_service(self, building_repository: SABuildingRepository) -> BuildingService:
        """Provides the BuildingService for managing buildings.

        Args:
            building_repository (SABuildingRepository): Repository instance for building entities.

        Returns:
            BuildingService: A service instance for handling building logic.
        """
        return BuildingService(building_repository)

    @provide(scope=Scope.REQUEST)
    def organization_service(
        self,
        organization_repository: SAOrganizationRepository,
        building_repository: SABuildingRepository,
        activity_repository: SAActivityRepository,
        organization_activity_repository: SAOrganizationActivityRepository,
    ) -> OrganizationService:
        """Provides the OrganizationService for managing organizations.

        Args:
            organization_repository (SAOrganizationRepository): Repository instance for organization entities.
            building_repository (SABuildingRepository): Repository instance for building entities.
            activity_repository (SAActivityRepository): Repository instance for activity entities.
            organization_activity_repository (SAOrganizationActivityRepository): Repository instance
                for organization activity entities.

        Returns:
            OrganizationService: A service instance for handling organization logic.
        """
        return OrganizationService(
            organization_repository,
            building_repository,
            activity_repository,
            organization_activity_repository,
        )
