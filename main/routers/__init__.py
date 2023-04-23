from src.routers.auth import auth_router

APP_BLUEPRINTS = [auth_router]

__all__ = tuple(k for k in locals() if not k.startswith("_"))
