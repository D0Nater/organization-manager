"""Dataclass repository."""

from typing import Any, ClassVar, Protocol, Self


class Dataclass(Protocol):
    """Dataclass."""

    # as already noted in comments, checking for this attribute is currently
    # the most reliable way to ascertain that something is a dataclass
    __dataclass_fields__: ClassVar[dict[str, Any]]


class DataclassFromDict(Dataclass, Protocol):
    """Dataclass from dict."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Creates a dataclass instance from a dictionary, validating provided data."""
