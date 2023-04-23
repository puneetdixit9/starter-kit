from sqlalchemy import event

from main.modules.auth.model import AuthUser
from main.modules.user.model import User


@event.listens_for(AuthUser, "after_insert")
def auth_user_created_listener(mapper, connection, target):
    user = User.create({User.username: target.username, User.email: target.email, User.id: target.id})
    print(user)
