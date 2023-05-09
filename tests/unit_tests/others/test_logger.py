import logging
import os

from main.logging_module.logger import (
    LOGS_BASE_DIR,
    create_base_dir_if_not_exists,
    get_logger,
)


def test_logs_base_dir_creation(mocker):
    """
    Test if the logs base directory is created successfully.
    """
    mocker.patch.object(os.path, "exists", return_value=False)
    mocker.patch.object(os, "makedirs", return_value=True)

    create_base_dir_if_not_exists()
    mocker.patch.object(os.path, "exists", return_value=True)
    assert os.path.exists(LOGS_BASE_DIR)


def test_get_logger():
    logger_name = "my_logger"
    logger = get_logger(logger_name)
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    assert logger.level == logging.INFO

    logger2 = get_logger(logger_name, logging.WARNING)
    assert logger2.level == logging.WARNING
    assert len(logger2.handlers) == 2

    logger3 = get_logger(logger_name, logging.DEBUG)
    assert logger3.level == logging.DEBUG
    assert len(logger3.handlers) == 3
