"""Coordinate entity."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Coordinate:
    """Value Object for Geographic Coordinate.

    Represents a geographic point with latitude and longitude.
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        """Validate coordinate boundaries.

        Raises:
            ValueError: If latitude or longitude are out of valid range.
        """
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError(f"Invalid latitude: {self.latitude}. Must be between -90 and 90 degrees.")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError(f"Invalid longitude: {self.longitude}. Must be between -180 and 180 degrees.")

    @classmethod
    def from_tuple(cls, coord: tuple[float, float]) -> Self:
        """Create Coordinate from (latitude, longitude) tuple.

        Args:
            coord (tuple[float, float]): A tuple containing latitude and longitude.

        Returns:
            Self: A Coordinate instance.
        """
        lat, lon = coord
        return cls(latitude=lat, longitude=lon)

    def to_tuple(self) -> tuple[float, float]:
        """Convert Coordinate to tuple.

        Returns:
            tuple[float, float]: (latitude, longitude)
        """
        return (self.latitude, self.longitude)

    def __str__(self) -> str:
        """String representation of the coordinate."""
        return f"({self.latitude:.6f}, {self.longitude:.6f})"
