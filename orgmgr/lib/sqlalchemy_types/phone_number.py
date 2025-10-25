"""PhoneNumber SQLAlchemy type."""

from sqlalchemy import JSON, Dialect, TypeDecorator

from orgmgr.lib.entities.phone_number import PhoneNumber


class PhoneNumberType(TypeDecorator[list[PhoneNumber] | None]):
    """Custom SQLAlchemy type for PhoneNumber value object."""

    impl = JSON
    cache_ok = True

    def process_bind_param(self, value: list[PhoneNumber] | None, dialect: Dialect) -> list[str] | None:
        """Convert PhoneNumber value object into string before saving into DB.

        Args:
            value (list[PhoneNumber] | None): PhoneNumber value object to convert.
            dialect (Dialect): SQLAlchemy dialect currently in use.

        Returns:
            list[str] | None: Phone number string in international format, or None.
        """
        if value is None:
            return None
        return [pn.number for pn in value]

    def process_result_value(self, value: str | None, dialect: Dialect) -> list[PhoneNumber] | None:
        """Convert string from DB into PhoneNumber value object.

        Args:
            value (str | None): Stored string from DB.
            dialect (Dialect): SQLAlchemy dialect currently in use.

        Returns:
            list[PhoneNumber] | None: PhoneNumber value object created from DB value.
        """
        if value is None:
            return None
        return [PhoneNumber(number=s) for s in value]
