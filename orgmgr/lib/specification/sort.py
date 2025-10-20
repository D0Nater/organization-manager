"""Sort specification."""

from copy import copy
from types import EllipsisType
from typing import Self

from orgmgr.lib.enums.sort import OrderByType


class SortSpecification:
    """Sort specification for a field with optional direction."""

    def __init__(self, field: str, direction: OrderByType | EllipsisType = ...):
        """Initialize a SortSpecification with a field and an optional direction.

        Args:
            field (str): The name of the field to sort by.
            direction (OrderByType | EllipsisType): The sort direction, or EllipsisType to defer specification.
        """
        self.field = field
        self._direction = direction

    @property
    def direction(self) -> OrderByType:
        """Get the sort direction if specified, otherwise raises AttributeError.

        Returns:
            OrderByType: The sort direction associated with the field.

        Raises:
            AttributeError: If the direction is not yet specified and remains EllipsisType.
        """
        if isinstance(self._direction, EllipsisType):
            raise AttributeError("Need create spec instance with direction by `new_with_direction`")
        return self._direction

    def new_with_direction(self, direction: OrderByType) -> Self:
        """Create a new SortSpecification instance with the given direction applied.

        Args:
            direction (OrderByType): The sort direction to apply to the field.

        Returns:
            Self: A new SortSpecification instance with the specified direction.
        """
        x = copy(self)
        x._direction = direction
        return x
