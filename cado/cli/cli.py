import logging
import pkg_resources
import webbrowser
from pathlib import Path

import click
import uvicorn

from cado.app.app import app as cado_app

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


@main.command(name="up")
@click.option("--host", type=str, default="localhost")
@click.option("--port", "-p", type=int, default=8000)
@click.option("--debug", is_flag=True, default=False)
@click.option("--log-level", type=int, default=logging.INFO)
@click.option("--open/--no-open", is_flag=True, default=True)
def up_command(host: str, port: int, debug: bool, log_level: int, open: bool) -> None:
    """Command to start up cado app."""
    current_dirpath = Path(__file__).parent
    cado_string = """
                 _
                ( )
   ___   _ _   _| |  _
 / ___)/ _  )/ _  |/ _ \\
( (___( (_| | (_| | (_) )
 \\____)\\__ _)\\__ _)\\___/
"""

    print("\033[0;32m")
    print(cado_string)

    package_version = pkg_resources.get_distribution("cado").version
    print(f"\nRunning cado version {package_version}\n")

    url = f"http://{host}:{port}"
    print(f"\nOpen \033[00m [[ \033[0;34m {url} \033[00m ]] \033[0;32m in a browser to get started")

    print("\033[00m")

    if open:
        webbrowser.open(url)

    logger.info(f"Starting app from {current_dirpath}")

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
