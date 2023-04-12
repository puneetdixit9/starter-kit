from flask_jwt_extended import JWTManager

from src.managers.auth import AuthManager

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    return AuthManager.token_revoked_check(jwt_payload)
