import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.expanduser("~"), "Desktop", "starter_app.env")
load_dotenv(dotenv_path)
