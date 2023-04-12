from src.managers.auth import ROLE, AuthManager
from src.managers.jwt import jwt
from src.managers.main import MainManager

all = tuple(ROLE, AuthManager, MainManager, jwt)
