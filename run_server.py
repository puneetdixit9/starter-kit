from project import get_app
import settings

app = get_app(settings.CONFIG)

if __name__ == "__main__":
    app.run()
