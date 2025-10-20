"""Base classes for schemas."""

from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Sequence
from typing import Any, Self, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.config import JsonDict

from orgmgr.lib.specification.field import FieldSpecification
from orgmgr.lib.specification.sort import SortSpecification


T = TypeVar("T")


class BaseSchema(BaseModel, ABC):
    """Base schema class for Pydantic models with common utilities."""

    model_config = ConfigDict(from_attributes=True)

    def iterate_set_fields(self, exclude: Sequence[str] | None = None) -> Generator[tuple[str, Any], None, None]:
        """Iterate over fields that have been explicitly set on the schema, optionally excluding some fields.

        Args:
            exclude (Sequence[str] | None): Optional list of field names to exclude from iteration. Defaults to None.

        Yields:
            tuple[str, Any]: A tuple containing the field name and its value for each explicitly set field.
        """
        model_fields_set = self.model_fields_set - set(exclude or [])

        for field_name in model_fields_set:
            attr = getattr(self, field_name)
            yield field_name, attr

    def iterate_set_fields_info(self) -> Generator[tuple[str, JsonDict], None, None]:
        """Iterate over metadata information of fields that have non-null values.

        Yields:
            tuple[str, JsonDict]: A tuple containing the field name and its associated JSON schema metadata.
        """
        for field_name, field_info in self.__pydantic_fields__.items():
            field_value = getattr(self, field_name)
            if field_value is None:
                continue

            if isinstance(field_info.json_schema_extra, dict):
                yield field_name, field_info.json_schema_extra
            else:
                yield field_name, field_info._inititial_kwargs if hasattr(field_info, "_inititial_kwargs") else {}


class BaseEntitySchema[T](BaseSchema, ABC):
    """Base schema for entities with conversion methods between entities and schemas."""

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: T) -> Self:
        """Creates a schema instance from the given entity.

        Args:
            entity (T): The entity object to convert into a schema.

        Returns:
            Self: A new schema instance populated with entity data.
        """
        raise NotImplementedError


class BaseEntityCreateSchema[T](BaseSchema, ABC):
    """Abstract base schema for creating entities."""

    @abstractmethod
    def to_entity(self, **kwargs: Any) -> T:
        """Convert the schema into its corresponding entity representation.

        Returns:
            T: The entity representation created from the schema.
        """
        raise NotImplementedError


class BaseEntityUpdateSchema[T](BaseSchema):
    """Base schema for updating existing entities."""

    def update_entity(self, entity: T, exclude: Sequence[str] | None = None) -> T:
        """Update the given entity with fields set in the schema.

        Args:
            entity (T): The entity instance to update.
            exclude (Sequence[str] | None): Optional list of field names to exclude from update. Defaults to None.

        Returns:
            T: The updated entity with fields modified according to the schema.
        """
        for k, v in self.iterate_set_fields(exclude):
            setattr(entity, k, v)

        return entity


class BaseFilterSchema(BaseSchema):
    """Base filter schema."""

    def to_specifications(self) -> list[FieldSpecification[BaseSchema, Any]]:
        """Convert schema fields with FieldSpecification into a list of specifications with assigned values.

        Returns:
            list[FieldSpecification[BaseSchema, Any]]: A list of field specifications built from the schema.
        """
        return self._collect_specs(
            FieldSpecification,  # type: ignore[type-abstract]
            lambda spec, value: spec.new_with_value(value),
        )

    def to_sort_specifications(self) -> list[SortSpecification]:
        """Convert schema fields with SortSpecification into a list of sort specifications with directions.

        Returns:
            list[SortSpecification]: A list of sort specifications built from the schema.
        """
        return self._collect_specs(
            SortSpecification,
            lambda spec, direction: spec.new_with_direction(direction),
        )

    def _collect_specs(self, spec_type: type[T], build: Callable[[T, Any], T]) -> list[T]:
        """Collect specifications of the given type from set fields and build them using the provided builder function.

        Args:
            spec_type (type[T]): The specification class type to filter against
                (e.g., FieldSpecification or SortSpecification).
            build (Callable[[T, Any], T]): A function that takes a specification instance
                and a field value, returning a new spec.

        Returns:
            list[T]: A list of built specifications of the given type.
        """
        specs = list[T]()

        for field_name, field_info in self.iterate_set_fields_info():
            field_spec: Any = field_info.get("specification", None)
            if isinstance(field_spec, spec_type):
                specs.append(build(field_spec, getattr(self, field_name)))

        return specs
