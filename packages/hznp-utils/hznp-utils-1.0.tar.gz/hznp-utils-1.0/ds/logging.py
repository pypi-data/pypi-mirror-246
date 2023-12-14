import logging
import logging.config
import os

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

def get_log_config(log_name: str, level) -> dict:
    """Returns a logging config dict for use in logging.config.dictConfig

    Args:
        log_name (str): file that will be using the logger

    Returns:
        dict: dict of config for logging streams
    """

    LOGGING_CONFIG = {
        "version": 1,
        "loggers": {
            "": {  # root logger
                "level": f"{level}",
                "handlers": [
                    "debug_console_handler",
                ],
            },
        },
        "handlers": {
            "debug_console_handler": {
                "level": f"{level}",
                "formatter": "info",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
          
        },
        "formatters": {
            "info": {
                "format": "%(asctime)s-%(levelname)s-%(name)s::|%(lineno)s:: %(message)s"
            },
            "error": {
                "format": "%(asctime)s-%(levelname)s-%(name)s::|%(lineno)s:: %(message)s"
            },
        },
    }

    return LOGGING_CONFIG


def get_logger(log_name: str, level='DEBUG') -> logging.Logger:
    """Creates a logging object

    Args:
        log_name (str): name of logger


    Returns:
        logging.Logger: the current logger used by the file
    """

    logging.config.dictConfig(get_log_config(log_name, level))

    # Get the logger specified in the file
    logger = logging.getLogger(log_name)
    
    gcloud_logging_client = google.cloud.logging.Client()
    
    gcloud_logging_handler = CloudLoggingHandler(gcloud_logging_client, name=log_name)
    gcloud_logging_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(gcloud_logging_handler)
    return logger
