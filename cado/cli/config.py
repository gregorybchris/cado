import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_ui_config(port: int) -> None:
    static_dirpath = Path(__file__).resolve().parent.parent / "ui" / "dist"
    config_filepath = static_dirpath / "config.json"
    with config_filepath.open("w") as f:
        config = {
            "port": port,
        }
        json.dump(config, f)

    logger.info("Wrote config to file %s: \n %s", config_filepath, config_filepath.read_text())
