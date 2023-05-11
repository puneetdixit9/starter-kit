from flask import Flask

from main import get_app


def test_flask_env_not_set():
    app = get_app()
    assert app is not None
    assert isinstance(app, Flask)
