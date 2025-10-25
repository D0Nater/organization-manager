"""Base SQLAlchemy filter."""

from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import Select


class BaseSQLAlchemyFilter[V](ABC):
    """An abstract base class for SQLAlchemy filters that operate on a value.

    This class serves as a template for filters that modify a SQLAlchemy query
    based on an input value. Subclasses must implement the `set_filter` method.
    """

    def __init__(self, value: V):
        """Initializes the filter with a value.

        Args:
            value (V): The value to be used for filtering.
        """
        self.value = value

    @abstractmethod
    def set_filter(self, query: Select[Any]) -> Select[Any]:
        """Applies the filter to a SQLAlchemy query.

        Args:
            query (Select[Any]): The SQLAlchemy query object to apply the filter to.

        Returns:
            Select[Any]: The modified query with the filter applied.
        """
