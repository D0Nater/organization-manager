"""Action provider."""

from dishka import Provider, Scope, provide

from orgmgr.implementations.actions import SAActivityAction
from orgmgr.implementations.repositories.activity import SAActivityRepository


class ActionProvider(Provider):
    """Provider for action instances."""

    @provide(scope=Scope.REQUEST)
    def activity_action(self, activity_repository: SAActivityRepository) -> SAActivityAction:
        """Provides a SQLAlchemy-based action for activity entities.

        Args:
            activity_repository (SAActivityRepository): Repository for activity persistence.

        Returns:
            SAActivityAction: An action instance for managing activity entities.
        """
        return SAActivityAction(activity_repository)
