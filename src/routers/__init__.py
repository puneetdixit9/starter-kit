from src.routers.auth import auth_router
from src.routers.main import main_router

APP_BLUEPRINTS = [
    auth_router,
    main_router
]