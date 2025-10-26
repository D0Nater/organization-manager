"""Base SQLAlchemy repository."""

from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from orgmgr.lib.models import BaseModel


class SABaseRepository[ID, E, M: BaseModel[Any]]:
    """Generic SQLAlchemy base repository for managing CRUD operations on models.

    This repository provides common methods for creating, retrieving, updating, and deleting entities.
    It uses SQLAlchemy's AsyncSession and requires that the model extends AbstractModel with proper entity conversion.
    """

    model: type[M]
    pk_name: str = "id"

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with the provided database session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session used for database operations.
        """
        self._session = session

    async def create(self, entity: E) -> E:
        """Create a new entity in the database and return it.

        Args:
            entity (E): The entity object to persist.

        Returns:
            E: The persisted entity with updated state (e.g., primary key).
        """
        model = self.model.from_entity(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()

    async def get_by_id(self, entity_id: ID) -> E | None:
        """Retrieve a single entity by its primary key.

        Args:
            entity_id (ID): The primary key value of the entity to retrieve.

        Returns:
            E | None: The entity if found, otherwise None.
        """
        stmt = select(self.model).where(getattr(self.model, self.pk_name) == entity_id)
        res = await self._session.execute(stmt)
        m = res.scalar_one_or_none()
        return m.to_entity() if m else None

    async def update(self, entity: E) -> E:
        """Update an existing entity in the database and return it.

        Args:
            entity (E): The entity object with updated data.

        Returns:
            E: The updated entity.
        """
        model = self.model.from_entity(entity)
        await self._session.merge(model)
        await self._session.flush()
        return model.to_entity()

    async def delete(self, entity_id: ID) -> None:
        """Delete a single entity by its primary key.

        Args:
            entity_id (ID): The primary key value of the entity to delete.

        Returns:
            None
        """
        stmt = delete(self.model).where(getattr(self.model, self.pk_name) == entity_id)
        await self._session.execute(stmt)
