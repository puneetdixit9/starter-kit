from flask_migrate import MigrateCommand
from flask_script import Command, Manager

from main import get_app

app = get_app()


manager = Manager(app)
manager.add_command("db", MigrateCommand)


class RunServer(Command):
    """
    Custom Flask-Script command to start the Flask development server with debugging enabled.
    """

    def run(self):
        app.run(debug=True)


manager.add_command("runserver", RunServer())

if __name__ == "__main__":
    manager.run()
