from flask import Blueprint
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.automation.routes import covid_questionnaire_completed

main = Blueprint("main", __name__)


@main.route('/')     # the route that will be used in the browser
@main.route('/home')
@login_required
def home():
    if not covid_questionnaire_completed(current_user.id):
        flash("Before moving on please complete the form below", 'warning')
        return redirect(url_for('automation.covid_questionnaire'))
    return render_template('home.html')




