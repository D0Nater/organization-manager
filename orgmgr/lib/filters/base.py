"""Base filter."""

from abc import ABC, abstractmethod


class BaseFilter[V, Q](ABC):
    """An abstract base class for filters that operate on a value.

    This class serves as a template for filters that modify a query
    based on an input value. Subclasses must implement the `set_filter` method.
    """

    def __init__(self, value: V):
        """Initializes the filter with a value.

        Args:
            value (V): The value to be used for filtering.
        """
        self.value = value

    @abstractmethod
    def set_filter(self, query: Q) -> Q:
        """Applies the filter to a query.

        Args:
            query (Q): The query object to apply the filter to.

        Returns:
            Q: The modified query with the filter applied.
        """
