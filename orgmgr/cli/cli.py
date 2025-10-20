"""Module with main CLI function."""

import click

from orgmgr.lib.utils.log import configure_logging


@click.group()
def cli() -> None:
    """Entry point for the CLI control interface.

    This command group serves as the root for all subcommands and configures logging before execution.
    """
    configure_logging()
