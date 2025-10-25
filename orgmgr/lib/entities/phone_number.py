"""Phone number entity."""

from dataclasses import dataclass
from re import fullmatch
from typing import Self


@dataclass(frozen=True)
class PhoneNumber:
    """Value Object for a Phone Number.

    Represents a phone number in international format, e.g., '+1234567890'.
    """

    number: str

    def __post_init__(self) -> None:
        """Validate the phone number format.

        Raises:
            ValueError: If the phone number is not in a valid international format.
        """
        if not fullmatch(r"\+\d{6,15}", self.number):
            raise ValueError(
                f"Invalid phone number: {self.number}. Must be in international format, e.g., '+1234567890'."
            )

    @classmethod
    def from_parts(cls, country_code: str, local_number: str) -> Self:
        """Create PhoneNumber from country code and local number.

        Args:
            country_code (str): The country code with or without '+'.
            local_number (str): The local number digits.

        Returns:
            Self: A PhoneNumber instance.
        """
        cc = country_code if country_code.startswith("+") else f"+{country_code}"
        return cls(number=f"{cc}{local_number}")
