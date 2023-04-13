import logging

import settings


def get_handler(name, log_level=settings.INFO):
    handler = logging.FileHandler(settings.LOGS_BASE_DIR + f"/{name}.log")
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    return handler


def get_logger(name, log_level=settings.INFO):
    access_logger = logging.getLogger(name)
    access_logger.setLevel(log_level)
    handler = get_handler(name, log_level)
    access_logger.addHandler(handler)
    return access_logger
