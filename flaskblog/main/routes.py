from flask import Blueprint
from flask import render_template
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint("main", __name__)


@main.route('/')     # the route that will be used in the browser
@main.route('/home')
@login_required
def home():
    return render_template('home.html')




