"""Field specification."""

from collections.abc import Callable, Sequence
from copy import copy
from re import match as re_match
from types import EllipsisType
from typing import Any, Self, TypeVar

from orgmgr.lib.specification.base import Specification
from orgmgr.lib.utils.rattrs import rgetattr


T = TypeVar("T")


class FieldSpecification[T, V](Specification[T]):
    """Generic field-bound specification that can defer a value until bound via new_with_value()."""

    description = "Generic field-bound specification; holds a field name and a deferred or concrete value."

    def __init__(self, field: str, value: V | EllipsisType = ...):
        """Initialize a FieldSpecification with a field name and an optional deferred value.

        Args:
            field (str): The dotted path or attribute name to read from objects.
            value (V | EllipsisType): The value to compare against, or EllipsisType to defer binding.
        """
        super().__init__()
        self.field = field
        self._value = value

    @property
    def value(self) -> V:
        """Return the bound value if present; raises AttributeError if the value is still deferred.

        Returns:
            V: The concrete value bound to this specification.

        Raises:
            AttributeError: If the value is not yet bound (was initialized with EllipsisType).
        """
        if isinstance(self._value, EllipsisType):
            raise AttributeError("Need create spec instance with value by `new_with_value`")
        return self._value

    def new_with_value(self, value: V) -> Self:
        """Return a new FieldSpecification cloned from this one with the given value bound.

        Args:
            value (V): The concrete value to bind to the specification.

        Returns:
            Self: A new instance with the provided value bound.
        """
        x = copy(self)
        x._value = value
        return x


class EqualsSpecification(FieldSpecification[T, Any]):
    """Specification that matches objects whose field value equals the bound value."""

    description = "Matches when rgetattr(obj, field) == value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if the object's field equals the bound value; otherwise False.

        Args:
            obj (T): The object to test against the specification.

        Returns:
            bool: True if equal, False otherwise.
        """
        return rgetattr(obj, self.field) == self.value


class NotEqualsSpecification(FieldSpecification[T, Any]):
    """Specification that matches objects whose field value does not equal the bound value."""

    description = "Matches when rgetattr(obj, field) != value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if the object's field does not equal the bound value; otherwise False.

        Args:
            obj (T): The object to test against the specification.

        Returns:
            bool: True if not equal, False otherwise.
        """
        return rgetattr(obj, self.field) != self.value


class GreaterThanSpecification(FieldSpecification[T, Any]):
    """Specification that matches objects whose field value is strictly greater than the bound value."""

    description = "Matches when rgetattr(obj, field) > value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if rgetattr(obj, self.field) > bound value; otherwise False.

        Args:
            obj (T): The object to test against the specification.

        Returns:
            bool: True if the object's field value is greater than the bound value; otherwise False.
        """
        return rgetattr(obj, self.field) > self.value


class LessThanSpecification(FieldSpecification[T, Any]):
    """Specification that matches objects whose field value is strictly less than the bound value."""

    description = "Matches when rgetattr(obj, field) < value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if rgetattr(obj, self.field) < bound value; otherwise False.

        Args:
            obj (T): The object to test against the specification.

        Returns:
            bool: True if the object's field value is less than the bound value; otherwise False.
        """
        return rgetattr(obj, self.field) < self.value


class GreaterThanOrEqualsToSpecification(FieldSpecification[T, Any]):
    """Specification that matches objects whose field value is greater than or equal to the bound value."""

    description = "Matches when rgetattr(obj, field) >= value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if rgetattr(obj, self.field) >= bound value; otherwise False.

        Args:
            obj (T): The object to test against the specification.

        Returns:
            bool: True if the object's field value is greater than or equal to the bound value; otherwise False.
        """
        return rgetattr(obj, self.field) >= self.value


class LessThanOrEqualsToSpecification(FieldSpecification[T, Any]):
    """Specification that matches objects whose field value is less than or equal to the bound value."""

    description = "Matches when rgetattr(obj, field) <= value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if rgetattr(obj, self.field) <= bound value; otherwise False.

        Args:
            obj (T): The object to test against the specification.

        Returns:
            bool: True if the object's field value is less than or equal to the bound value; otherwise False.
        """
        return rgetattr(obj, self.field) <= self.value


class FunctionSpecification(FieldSpecification[T, Any]):
    """Specification that evaluates a user-provided predicate against (obj, field, value)."""

    description = "Matches when func(obj, field, value) returns True."

    def __init__(
        self,
        field: str,
        func: Callable[[Any, str, Any], bool] = lambda _x, _y, _z: False,
        value: Any | EllipsisType = ...,
    ) -> None:
        """Initialize a FunctionSpecification with a field, a predicate function, and an optional deferred value.

        Args:
            field (str): The dotted path or attribute name to read from objects.
            func (Callable[[Any, str, Any], bool]): Predicate receiving (obj, field, value); must return bool.
            value (Any | EllipsisType): The comparison value, or EllipsisType to defer binding.
        """
        super().__init__(field, value)
        self.func = func

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if func(obj, field, value) evaluates to True; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: The predicate result.
        """
        return self.func(obj, self.field, self.value)


class InListSpecification(FieldSpecification[T, Sequence[Any]]):
    """Specification that checks membership of the field value in the bound sequence."""

    description = "Matches when rgetattr(obj, field) in value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if rgetattr(obj, field) is in the bound sequence; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if member, False otherwise.
        """
        return rgetattr(obj, self.field) in self.value


class NotInListSpecification(FieldSpecification[T, Sequence[Any]]):
    """Specification that checks non-membership of the field value in the bound sequence."""

    description = "Matches when rgetattr(obj, field) not in value."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if rgetattr(obj, field) is not in the bound sequence; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if not a member, False otherwise.
        """
        return rgetattr(obj, self.field) not in self.value


class SubListSpecification(FieldSpecification[T, Sequence[Any]]):
    """Specification that checks if the bound sequence is a subset of the object's field sequence."""

    description = "Matches when set(value) ⊆ set(rgetattr(obj, field))."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if set(value) is a subset of set(rgetattr(obj, field)); otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if subset, False otherwise.
        """
        return set(self.value).issubset(set(rgetattr(obj, self.field)))


class NotSubListSpecification(FieldSpecification[T, Sequence[Any]]):
    """Specification that checks that the bound sequence is not a subset of the object's field sequence."""

    description = "Matches when set(value) ⊄ set(rgetattr(obj, field))."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if set(value) is not a subset of set(rgetattr(obj, field)); otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if not a subset, False otherwise.
        """
        return not set(self.value).issubset(set(rgetattr(obj, self.field)))


class LikeSpecification(FieldSpecification[T, str]):
    """Specification that performs a SQL-like pattern match (case-sensitive) using % as a wildcard."""

    description = "Matches when field string satisfies LIKE pattern in value (case-sensitive, % → .*, dots escaped)."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if the field string matches the LIKE-style regex derived from value; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if pattern matches, False otherwise.
        """
        return re_match(self.value.replace("%", ".*").replace(".", r"\."), rgetattr(obj, self.field)) is not None


class NotLikeSpecification(LikeSpecification[T]):
    """Specification that negates LikeSpecification."""

    description = "Matches when LikeSpecification does not match."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if LikeSpecification would return False; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: Negated LIKE result.
        """
        return not super().is_satisfied_by(obj)


class ILikeSpecification(FieldSpecification[T, str]):
    """Specification that performs a case-insensitive SQL-like match by lowercasing the field value."""

    description = "Matches when lower(field) satisfies LIKE pattern in value (case-insensitive)."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if lowercased field matches the LIKE-style regex derived from value; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if pattern matches, False otherwise.
        """
        return (
            re_match(self.value.replace("%", ".*").replace(".", r"\."), rgetattr(obj, self.field).lower()) is not None
        )


class NotILikeSpecification(ILikeSpecification[T]):
    """Specification that negates ILikeSpecification."""

    description = "Matches when ILikeSpecification does not match."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if ILikeSpecification would return False; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: Negated ILIKE result.
        """
        return not super().is_satisfied_by(obj)


class IsNoneSpecification(FieldSpecification[T, bool]):
    """Specification that checks None-ness per a boolean flag (True → is None; False → is not None)."""

    description = "True means field must be None; False means field must not be None."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if the field matches the None-ness indicated by the bound boolean; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if the condition holds, False otherwise.

        Raises:
            AttributeError: If the value is not bound (initialized with EllipsisType).
        """
        return (rgetattr(obj, self.field) is None) if self.value else (rgetattr(obj, self.field) is not None)


class IsNotNoneSpecification(FieldSpecification[T, bool]):
    """Specification that checks not-None-ness per a boolean flag (True → is not None; False → is None)."""

    description = "True means field must not be None; False means field must be None."

    def is_satisfied_by(self, obj: T) -> bool:
        """Return True if the field matches the not-None-ness indicated by the bound boolean; otherwise False.

        Args:
            obj (T): The object to test.

        Returns:
            bool: True if the condition holds, False otherwise.

        Raises:
            AttributeError: If the value is not bound (initialized with EllipsisType).
        """
        return (rgetattr(obj, self.field) is not None) if self.value else (rgetattr(obj, self.field) is None)
