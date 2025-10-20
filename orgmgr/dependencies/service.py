"""Service provider."""

from dishka import Scope, provide
from dishka.integrations.fastapi import FastapiProvider

from orgmgr.implementations.repositories import SAActivityRepository
from orgmgr.services import ActivityService


class ServiceProvider(FastapiProvider):
    """Provider for service layer instances."""

    @provide(scope=Scope.REQUEST)
    def api_key_service(self, api_key_repository: SAActivityRepository) -> ActivityService:
        """Provides the ActivityService for managing activities.

        Args:
            api_key_repository (SAActivityRepository): Repository instance for activity entities.

        Returns:
            ActivityService: A service instance for handling activity logic.
        """
        return ActivityService(api_key_repository)
