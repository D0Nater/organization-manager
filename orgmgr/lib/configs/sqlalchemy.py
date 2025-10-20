"""SQLAlchemy config."""

from orgmgr.lib.configs.base import BaseConfig


class SQLAlchemyConfig(BaseConfig):
    """SQLAlchemy config.

    This config is used to configure the sqlalchemy.

    Attributes:
        url (str): The url of the sqlalchemy.
    """

    url: str
