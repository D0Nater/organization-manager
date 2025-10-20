"""Pagination schemas."""

from collections.abc import Sequence
from typing import Any, ClassVar, Self

from orgmgr.lib.entities.page import Page

from . import fields as f
from .base import BaseEntitySchema, BaseSchema


LIMIT = f.BaseField(description="Limit of items per page.", ge=1, le=100, default=10)
PAGE = f.BaseField(description="Page number.", ge=1, default=1)
ITEMS = f.BaseField(description="Response items.")
TOTAL_ITEMS = f.BaseField(description="Total items in the database.")
TOTAL_PAGES = f.BaseField(description="Total pages in the database.")


class PaginationRequest(BaseSchema):
    """Pagination request."""

    limit: int = LIMIT
    page: int = PAGE


class PaginationResponse[TBaseSchema: BaseSchema](BaseSchema):
    """Pagination response."""

    items: Sequence[TBaseSchema] = ITEMS
    total_items: int = TOTAL_ITEMS
    total_pages: int = TOTAL_PAGES


class EntityPaginationResponse[E, TBaseSchema: BaseEntitySchema[Any]](PaginationResponse[TBaseSchema]):
    """Entity pagination response."""

    _item_schema: ClassVar[type[TBaseSchema]]

    @classmethod
    def from_page(cls, page: Page[E]) -> Self:
        """Creates an EntityPaginationResponse instance from a paginated entity list.

        Args:
            page (Page[E]): A paginated object containing entity items, total count, and total number of pages.

        Returns:
            Self: An instance of EntityPaginationResponse populated with serialized entity data and pagination metadata.
        """
        return cls(
            items=[cls._item_schema.from_entity(i) for i in page.items],
            total_items=page.total,
            total_pages=page.pages,
        )
