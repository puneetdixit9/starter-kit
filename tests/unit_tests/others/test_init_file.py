from flask import Flask

from config import config_by_name
from main import get_app


def test_flask_env_not_set():
    app = get_app()
    assert app is not None
    assert isinstance(app, Flask)


def test_get_app_with_config():
    config = config_by_name["test"]
    app = get_app(config=config)
    assert isinstance(app, Flask)
