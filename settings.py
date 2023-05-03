import logging
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.expanduser("~"), "Desktop", "starter_app.env")
load_dotenv(dotenv_path)

LOGS_BASE_DIR = "logs"
if not os.path.exists(LOGS_BASE_DIR):
    os.makedirs(LOGS_BASE_DIR)
ERROR = logging.ERROR
INFO = logging.INFO
WARNING = logging.WARNING
