from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from utils import app
from dbs import MySQL
import functools

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


class User(UserMixin):
    def __init__(self, email):
        self.id = email
        sql = "SELECT email, pwd, permission, createTime FROM users WHERE email = \"%s\" " % email
        res = MySQL.select(sql, multi=False)
        self.pwd = res['pwd']
        self.permission = res['permission']
        self.createTime = res['createTime']

    @staticmethod
    def check_user(email, pwd):
        sql = "SELECT email FROM users WHERE email = \"%s\" AND pwd = \"%s\" " % (email, pwd)
        res = MySQL.select(sql, multi=False)
        if res is not None: return True
        return False


class LoginRequired:
    def __init__(self, param=''):
        self.allowed = []
        self.unallowed = []
        if param == '': return
        for arg in param.split(','):
            if arg[0] == '-':
                self.unallowed.append(arg[1:])
            else:
                self.allowed.append(arg)

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            print("Deco :", current_user.is_authenticated)
            if not current_user.is_authenticated:
                return "NOT LOGGED"
            if current_user.permission in self.unallowed:
                return "FORBIDDEN"
            if len(self.allowed) == 0 or current_user.permission in self.allowed:
                return fn(*args, **kwargs)
            else:
                return "NOT ALLOWED"

        return decorated
