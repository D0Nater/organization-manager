"""Page entity."""

from dataclasses import dataclass


@dataclass
class PaginationInfo:
    """Pagination parameters including page number and items per page.

    Attributes:
        page (int): 1-based index of the current page.
        per_page (int): Maximum number of items per page.
    """

    page: int
    per_page: int


@dataclass
class Page[T](PaginationInfo):
    """A single page of results with pagination metadata.

    Attributes:
        items (list[T]): Items on the current page.
        total (int): Total number of matching rows across all pages.
        page (int): 1-based index of the current page.
        per_page (int): Maximum number of items per page.
    """

    items: list[T]
    total: int

    @property
    def pages(self) -> int:
        """Calculate the total number of pages (ceil(total / per_page)).

        Returns:
            int: Total number of pages.
        """
        return (self.total + self.per_page - 1) // self.per_page

    @property
    def has_prev(self) -> bool:
        """Check whether there is a previous page.

        Returns:
            bool: True if a previous page exists, False otherwise.
        """
        return self.page > 1

    @property
    def has_next(self) -> bool:
        """Check whether there is a next page.

        Returns:
            bool: True if a next page exists, False otherwise.
        """
        return self.page < self.pages
