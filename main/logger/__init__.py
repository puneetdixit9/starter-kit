import logging
import os

ERROR = logging.ERROR
INFO = logging.INFO
WARNING = logging.WARNING


LOGS_BASE_DIR = "logs"


def create_base_dir_if_not_exists():
    if not os.path.exists(LOGS_BASE_DIR):
        os.makedirs(LOGS_BASE_DIR)


def get_handler(name: str, log_level=INFO):
    """
    This function is used to get a logger handler.
    :param name:
    :param log_level:
    :return:
    """
    create_base_dir_if_not_exists()
    handler = logging.FileHandler(LOGS_BASE_DIR + f"/{name}.log")
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    return handler


def get_logger(name: str, log_level=INFO):
    """
    This function is used to get a logger object.
    :param name:
    :param log_level:
    :return:
    """
    create_base_dir_if_not_exists()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    handler = get_handler(name, log_level)
    logger.addHandler(handler)
    return logger
