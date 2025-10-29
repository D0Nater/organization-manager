"""Base Unit of Work."""

from types import TracebackType
from typing import Protocol, Self


class BaseUnitOfWork(Protocol):
    """Base Unit of Work that manages a transaction."""

    async def __aenter__(self) -> Self:
        """Begins a transaction.

        Returns:
            Self: The instance of the Unit of Work class with a transaction started.
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits the transaction.

        Args:
            exc_type (type[BaseException] | None): The type of the exception raised, or None if no exception occurred.
            exc_val (BaseException | None): The exception object raised, or None if no exception occurred.
            exc_tb (TracebackType | None): The traceback object, or None if no exception occurred.
        """
