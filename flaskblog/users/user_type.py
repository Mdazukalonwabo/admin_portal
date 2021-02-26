from flask_login import current_user
from flaskblog.models import User


def permissions(*args, **kwargs):
    if current_user:
        print("im logged in")
