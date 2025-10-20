"""SQLAlchemy provider."""

from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from orgmgr.lib.configs.sqlalchemy import SQLAlchemyConfig


class SQLAlchemyProvider(Provider):
    """SQLAlchemy provider."""

    @provide(scope=Scope.APP)
    async def db_engine(self, sqlalchemy_config: SQLAlchemyConfig) -> AsyncEngine:
        """Creates and returns an asynchronous SQLAlchemy engine.

        Args:
            sqlalchemy_config (SQLAlchemyConfig): The database configuration object containing the connection URL.

        Returns:
            AsyncEngine: An asynchronous SQLAlchemy engine created from the provided configuration.
        """
        return create_async_engine(sqlalchemy_config.url)

    @provide(scope=Scope.APP)
    # Type ignore is needed because sessionmaker[AsyncSession] is not a subtype of sessionmaker[Session].
    async def db_session_maker(self, db_engine: AsyncEngine) -> sessionmaker[AsyncSession]:  # type: ignore[type-var]
        """Creates and returns an asynchronous session factory bound to the provided database engine.

        Args:
            db_engine (AsyncEngine): The SQLAlchemy asynchronous engine.

        Returns:
            sessionmaker[AsyncSession]: A session factory for creating AsyncSession instances.
        """
        # Type ignore is needed because for some reason SQLAlchemy doesn't understand the types properly.
        return sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore[call-overload]

    @provide(scope=Scope.REQUEST)
    async def db_session(
        self,
        # Type ignore is needed because sessionmaker[AsyncSession] is not a subtype of sessionmaker[Session].
        db_session_maker: sessionmaker[AsyncSession],  # type: ignore[type-var]
    ) -> AsyncGenerator[AsyncSession]:
        """Provides a per-request SQLAlchemy AsyncSession with commit/rollback lifecycle management.

        Args:
            db_session_maker (sessionmaker[AsyncSession]): The session factory used to create AsyncSession instances.

        Yields:
            AsyncSession: A new asynchronous session for database operations within the request lifecycle.

        Raises:
            SQLAlchemyError: If an error occurs during a database operation,
                the session is rolled back before re-raising.
        """
        session = db_session_maker()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            await session.close()
