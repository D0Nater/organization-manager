"""Server launch related commands."""

import os

import click
import uvicorn

from .cli import cli


@cli.command()
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to.")
@click.option("--port", "-p", default=8000, help="Port to bind to.")
@click.option("--reload", "-r", is_flag=True, help="Reload on code changes.")
@click.option("--workers", "-w", default=1, help="Number of workers.")
@click.option("--env", "-e", multiple=True, help="Environment variables in KEY=VALUE format.")
def run(host: str, port: int, reload: bool, workers: int, env: list[str]) -> None:
    """Runs the API webserver using Uvicorn with configurable options.

    Args:
        host (str): Host address to bind the server to. Defaults to "127.0.0.1".
        port (int): Port number to bind the server to. Defaults to 8000.
        reload (bool): Whether to reload on code changes. Useful for development. Defaults to False.
        workers (int): Number of worker processes to spawn. Defaults to 1.
        env (list[str]): List of environment variables in KEY=VALUE format to set before starting.
    """
    for key, value in [item.split("=") for item in env]:
        os.environ[key.upper()] = value

    uvicorn.run(
        "orgmgr.app:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        factory=True,
    )


@cli.command()
def dev() -> None:
    """Runs the development server with pre-defined settings."""
    os.environ["PRODUCTION"] = os.environ.get("PRODUCTION", "false")

    uvicorn.run(
        "orgmgr.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1,
        factory=True,
    )
