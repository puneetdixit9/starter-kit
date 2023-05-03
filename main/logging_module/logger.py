import logging

import settings


def get_handler(name: str, log_level=settings.INFO):
    """
    This function is used to get a logger handler.
    :param name:
    :param log_level:
    :return:
    """
    handler = logging.FileHandler(settings.LOGS_BASE_DIR + f"/{name}.log")
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    return handler


def get_logger(name: str, log_level=settings.INFO):
    """
    This function is used to get a logger object.
    :param name:
    :param log_level:
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    handler = get_handler(name, log_level)
    logger.addHandler(handler)
    return logger
