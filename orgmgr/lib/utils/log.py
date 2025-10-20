"""Logging utilities."""

import logging
import logging.config
from os import environ

from yaml import safe_load


def configure_logging() -> None:
    """Configure logging using environment variables or a YAML config file.

    This function sets up logging for the application. If the environment variable LOG_CONFIG is defined, the logging
    configuration is loaded from the specified YAML file. Otherwise, logging is configured using environment variables
    LOG_LEVEL, LOG_FORMAT, and LOG_FILE.

    Raises:
        ValueError: If LOG_LEVEL is defined but not a valid logging level.
        FileNotFoundError: If the path specified in LOG_CONFIG does not exist.
        yaml.YAMLError: If the YAML logging configuration file is invalid.
    """
    if log_config_path := environ.get("LOG_CONFIG"):
        with open(log_config_path) as f:
            logging_config = safe_load(f.read())
        logging.config.dictConfig(logging_config)
        return

    log_level = environ.get("LOG_LEVEL", "INFO").upper()

    if log_level not in logging.getLevelNamesMapping():
        raise ValueError(f"Invalid log level: {log_level}")

    log_format = environ.get("LOG_FORMAT", "%(asctime)s   %(name)-25s %(levelname)-8s %(message)s")
    log_file = environ.get("LOG_FILE")
    log_handlers = [
        logging.StreamHandler(),
        logging.FileHandler(log_file) if log_file else logging.NullHandler(),
    ]

    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)
