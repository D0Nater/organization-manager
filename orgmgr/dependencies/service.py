"""Service provider."""

from dishka import Scope, provide
from dishka.integrations.fastapi import FastapiProvider

from orgmgr.implementations.actions import SAActivityAction
from orgmgr.implementations.queries import SAActivityQuery, SABuildingQuery, SAOrganizationQuery
from orgmgr.implementations.repositories import SAActivityRepository, SABuildingRepository
from orgmgr.implementations.uow import SAOrganizationUnitOfWork
from orgmgr.lib.configs import AuthConfig
from orgmgr.services import ActivityService, AuthService, BuildingService, OrganizationService


class ServiceProvider(FastapiProvider):
    """Provider for service layer instances."""

    @provide(scope=Scope.REQUEST)
    def auth_service(self, auth_config: AuthConfig) -> AuthService:
        """Provides the AuthService.

        Args:
            auth_config (AuthConfig): AuthConfig instance for auth.

        Returns:
            AuthService: A service instance for handling auth logic.
        """
        return AuthService(auth_config)

    @provide(scope=Scope.REQUEST)
    def activity_service(
        self,
        activity_repository: SAActivityRepository,
        activity_query: SAActivityQuery,
        activity_action: SAActivityAction,
    ) -> ActivityService:
        """Provides the ActivityService for managing activities.

        Args:
            activity_repository (SAActivityRepository): Repository instance for activity entities.
            activity_query (SAActivityQuery): Query instance for activity entities.
            activity_action (SAActivityAction): Action instance for activity entities.

        Returns:
            ActivityService: A service instance for handling activity logic.
        """
        return ActivityService(activity_repository, activity_query, activity_action)

    @provide(scope=Scope.REQUEST)
    def building_service(
        self, building_repository: SABuildingRepository, building_query: SABuildingQuery
    ) -> BuildingService:
        """Provides the BuildingService for managing buildings.

        Args:
            building_repository (SABuildingRepository): Repository instance for building entities.
            building_query (SABuildingQuery): Query instance for building entities.

        Returns:
            BuildingService: A service instance for handling building logic.
        """
        return BuildingService(building_repository, building_query)

    @provide(scope=Scope.REQUEST)
    def organization_service(
        self,
        organization_uow: SAOrganizationUnitOfWork,
        organization_query: SAOrganizationQuery,
        building_repository: SABuildingRepository,
        activity_query: SAActivityQuery,
    ) -> OrganizationService:
        """Provides the OrganizationService for managing organizations.

        Args:
            organization_uow (SAOrganizationUnitOfWork): Organization Unit of Work instance.
            organization_query (SAOrganizationQuery): Query instance for organization entities.
            building_repository (SABuildingRepository): Repository instance for building entities.
            activity_query (SAActivityQuery): Query instance for activity entities.

        Returns:
            OrganizationService: A service instance for handling organization logic.
        """
        return OrganizationService(
            organization_uow,
            organization_query,
            building_repository,
            activity_query,
        )
