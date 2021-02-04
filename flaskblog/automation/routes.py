from flask import Blueprint
from flask import render_template, url_for, flash, redirect
from .forms import CovidQuestionsForm, LeaveRequestForm
from flaskblog.models import CovidQuestionnaire
from flaskblog import db
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

automation = Blueprint("automation", __name__)


@automation.route('/leave', methods=['GET', 'POST'])
@login_required
def leave():
    form = LeaveRequestForm()
    print()
    if form.validate_on_submit():
        print("im valid")
    return render_template('leave.html', form=form)


@automation.route("/covid-question", methods=['GET', 'POST'])
@login_required
def covid_questionnaire():
    if covid_questionnaire_completed(current_user.id):
        return redirect(url_for('home'))
    else:
        form = CovidQuestionsForm()
        if form.validate_on_submit():
            submitted_covid_questionnaire = CovidQuestionnaire(user_id=current_user.id,
                                                               temperature=int(form.temperature.data),
                                                               Shortness_of_breath=bool(form.Shortness_of_breath.data),
                                                               loss_of_taste_or_smell=bool(form.loss_of_taste_or_smell.data)
                                                               , contact_with_Covid=bool(form.contact_with_Covid.data),
                                                               diarrhea=bool(form.diarrhea.data),
                                                               nausea=bool(form.nausea.data),
                                                               sore_throat=bool(form.sore_throat.data),
                                                               nasal_congestion=bool(form.nasal_congestion.data))
            db.session.add(submitted_covid_questionnaire)
            db.session.commit()
            flash("Covid questionnaire answers submitted", 'success')
            return redirect(url_for('home'))
    return render_template('covid_questions.html', form=form)


def covid_questionnaire_completed(user_id):
    latest_questionnaire = CovidQuestionnaire.query.filter_by(user_id=user_id)
    todays_date = datetime.now().date()
    for i in latest_questionnaire:
        if todays_date == i.time_signed.date():
            return True
    return False


