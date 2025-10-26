"""Base SQLAlchemy filter."""

from typing import Any

from sqlalchemy import Select

from orgmgr.lib.filters.base import BaseFilter


class BaseSQLAlchemyFilter[V](BaseFilter[V, Select[Any]]):
    """An abstract base class for SQLAlchemy filters that operate on a value.

    This class serves as a template for filters that modify a SQLAlchemy query
    based on an input value. Subclasses must implement the `set_filter` method.
    """
