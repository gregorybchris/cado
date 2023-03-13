import logging
from pathlib import Path

import click
import uvicorn

from cado.app.app import app as cado_app


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--host", type=str, default="0.0.0.0")
@click.option("--port", "-p", type=int, default=8000)
@click.option("--debug", is_flag=True)
@click.option("--log-level", type=int, default=logging.INFO)
def up(host: str, port: int, debug: bool, log_level: int) -> None:
    print("Welcome to Cado IDE")
    current_dirpath = Path(__file__).parent
    print(f"From {current_dirpath}")
    print("Starting app")
    uvicorn.run(cado_app, host=host, port=port, debug=debug, log_level=log_level)
