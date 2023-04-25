# from flask_migrate import
# from flask_script import Manager

import settings
from main import get_app

app = get_app(settings.CONFIG)


# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    # manager.run()
    app.run(debug=True)
