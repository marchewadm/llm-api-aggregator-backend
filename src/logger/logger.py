import os
import json
import pathlib
import logging.config
import logging.handlers

logger = logging.getLogger(__name__)


def init_logging():
    config_file = pathlib.Path("src/logger/config.json")

    with open(config_file) as file:
        config = json.load(file)

    # Create the log directory if it does not exist
    log_file_path = config["handlers"]["file"]["filename"]
    log_dir = os.path.dirname(log_file_path)
    os.makedirs(log_dir, exist_ok=True)

    logging.config.dictConfig(config)
