from flask_login import LoginManager, UserMixin
from werkzeug import check_password_hash

from app.utils.mongo import Admins


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "/login/admin"
login_manager.login_message = "You are not authorized to access this page"
login_manager.login_message_category = "alert alert-danger"


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.authenticated = False
        self.active = False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)


@login_manager.user_loader
def load_user(username):
    return User(username)


def verify_credentials(username, password):
    try:
        admin = Admins.objects().get(username=username)
        if check_password_hash(admin.password, password):
            return True
        return False
    except (Admins.DoesNotExist, Admins.MultipleObjectsReturned):
        return False
