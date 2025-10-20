"""Base classes for database models."""

from abc import abstractmethod
from typing import Any, Self

from sqlalchemy.orm import DeclarativeBase


class BaseModel[T](DeclarativeBase):
    """Base database model providing common functionality for ORM models.

    This abstract base class enforces entity conversion methods (`from_entity`, `to_entity`).
    """

    __abstract__ = True

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: T) -> Self:
        """Converts an external entity into a corresponding ORM model instance.

        Args:
            entity (T): The entity object to be converted into a database model.

        Returns:
            Self: A new instance of the model created from the entity.
        """
        raise NotImplementedError

    @abstractmethod
    def to_entity(self) -> T:
        """Converts the ORM model into its corresponding external entity representation.

        Returns:
            T: The external entity representation of the model.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """Returns a detailed string representation of the model including primary key values.

        Returns:
            str: The developer-friendly string representation of the model.
        """
        _repr = f"<{self.__class__.__name__} "
        for name in self._get_primary_keys():
            _repr += f"{name}={self._get_key_value(name)}, "
        return _repr[:-2] + ">"

    def __str__(self) -> str:
        """Returns the string representation of the model.

        Returns:
            str: A user-friendly string representation of the model.
        """
        return self.__repr__()

    def to_dict(self) -> dict[str, Any]:
        """Returns the dictionary representation of the model, including its attributes.

        Returns:
            dict[str, Any]: A dictionary of model attributes and their values.
        """
        return self.__dict__

    @classmethod
    def _get_primary_keys(cls) -> list[str]:
        """Returns the names of primary key columns defined on the model.

        Returns:
            list[str]: A list of primary key column names.
        """
        return [i.name for i in cls.__table__.primary_key.columns.values()]  # type: ignore[attr-defined]

    def _get_key_value(self, name: str) -> Any:
        """Returns the value of the given primary key attribute.

        Args:
            name (str): The name of the primary key attribute.

        Returns:
            Any: The value of the specified primary key.
        """
        return getattr(self, name)
