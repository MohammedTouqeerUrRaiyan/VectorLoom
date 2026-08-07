import logging
import sys

from src.config.settings import settings


def setup_logger(name: str):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console = logging.StreamHandler(sys.stdout)

    console.setFormatter(formatter)

    logger.addHandler(console)

    logger.propagate = False

    return logger