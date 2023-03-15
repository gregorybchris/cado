import logging
from pathlib import Path

import click
import uvicorn

from cado.app.app import app as cado_app


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


@main.command(name="up")
@click.option("--host", type=str, default="0.0.0.0")
@click.option("--port", "-p", type=int, default=8000)
@click.option("--debug", is_flag=True)
@click.option("--log-level", type=int, default=logging.INFO)
def up_command(host: str, port: int, debug: bool, log_level: int) -> None:
    """Command to start up cado app."""
    print("Welcome to cado IDE")
    current_dirpath = Path(__file__).parent
    print(f"From {current_dirpath}")
    print("Starting app")

    package_dirpath = current_dirpath.parent.parent
    log_config_filepath = package_dirpath / "logging.yaml"
    uvicorn.run(
        cado_app,
        host=host,
        port=port,
        debug=debug,
        log_level=log_level,
        log_config=str(log_config_filepath),
    )
