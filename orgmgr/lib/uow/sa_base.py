"""Base SQLAlchemy Unit of Work."""

from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from .base import BaseUnitOfWork


class SABaseUnitOfWork(BaseUnitOfWork):
    """Base SQLAlchemy Unit of Work that manages a nested transaction.

    This class uses a nested transaction (`SAVEPOINT`) within an existing
    session, ensuring that database operations within the `with` block are
    atomic relative to the containing transaction. The transaction is committed
    on successful exit or rolled back on exception.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        """
        self._session = session
        self._transaction: AsyncSessionTransaction

    async def __aenter__(self) -> Self:
        """Begins a nested transaction within the session.

        Returns:
            Self: The instance of the SABaseUnitOfWork class with a nested transaction started.
        """
        self._transaction = self._session.begin_nested()
        await self._transaction.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits the nested transaction, handling commit, rollback, and cleanup.

        Args:
            exc_type (type[BaseException] | None): The type of the exception raised, or None if no exception occurred.
            exc_val (BaseException | None): The exception object raised, or None if no exception occurred.
            exc_tb (TracebackType | None): The traceback object, or None if no exception occurred.
        """
        await self._transaction.__aexit__(exc_type, exc_val, exc_tb)
