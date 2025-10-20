"""Database-related commands."""

import alembic.config

from .cli import cli


@cli.group()
def db() -> None:
    """Group of database management commands for migrations and schema versioning."""


@db.command()
def migrate() -> None:
    """Runs all pending Alembic migrations up to the latest head revision."""
    alembic.config.main(argv=["--raiseerr", "upgrade", "head"])


@db.command()
def upgrade() -> None:
    """Runs the next available Alembic migration (equivalent to +1 step)."""
    alembic.config.main(argv=["--raiseerr", "upgrade", "+1"])


@db.command()
def downgrade() -> None:
    """Reverts the database schema by one Alembic migration (equivalent to -1 step)."""
    alembic.config.main(argv=["--raiseerr", "downgrade", "-1"])
