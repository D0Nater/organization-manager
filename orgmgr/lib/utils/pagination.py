"""Pagination utilities."""

from typing import Any

from sqlalchemy import Select


def add_pagination_to_query(query: Select[Any], limit: int, page: int) -> Select[Any]:
    """Apply LIMIT/OFFSET to a SQLAlchemy Select.

    Args:
        query (Select[Any]): The query to paginate.
        limit (int): Items per page. Must be >= 1.
        page (int): 1-based page number. Must be >= 1.

    Returns:
        Select[Any]: The paginated Select.

    Raises:
        ValueError: If limit or page are less than 1.
    """
    if limit < 1:
        raise ValueError("limit must be >= 1")
    if page < 1:
        raise ValueError("page must be >= 1")

    offset = (page - 1) * limit
    return query.limit(limit).offset(offset)
