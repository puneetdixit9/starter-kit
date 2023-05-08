import logging
import os

from main.logging_module.logger import get_logger


def test_logs_base_dir_creation(tmpdir):
    """
    Test if the logs base directory is created successfully.
    """
    # Set the logs base directory to the temporary directory created by pytest
    LOGS_BASE_DIR = tmpdir.join("logs")
    assert not os.path.exists(LOGS_BASE_DIR)

    # Call the code that creates the logs base directory
    if not os.path.exists(LOGS_BASE_DIR):
        os.makedirs(LOGS_BASE_DIR)

    # Check if the logs base directory has been created successfully
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
