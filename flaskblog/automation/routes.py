from flask import Blueprint
from flask import render_template, url_for, flash, redirect
from .forms import CovidQuestionsForm, LeaveRequestForm
from flaskblog.models import CovidQuestionnaire, LeaveApplication, User, StaffMember
from flaskblog import db
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

automation = Blueprint("automation", __name__)


@automation.route('/leave', methods=['GET', 'POST'])
@login_required
def leave():
    # the leave request of the the user
    form = LeaveRequestForm()
    leave_applied = LeaveApplication.query.all()
    if form.validate_on_submit():
        user = StaffMember.query.filter_by(user_id=current_user.id).first()
        leave_application = LeaveApplication(user_id=user.id, category=search(form.leave_type.data),
                                             pre_authorisation=form.authorisation.data,
                                             personal_message=form.message.data, leave_date_from=form.start_date.data,
                                             leave_date_to=form.end_date.data)
        db.session.add(leave_application)
        db.session.commit()
        flash("Your leave application has been submitted", 'success')
    return render_template('leave.html', form=form, leaves=current_leave_applications(current_user))


def current_leave_applications(user):
    # returns the leaves applied for by the user
    my_leaves = LeaveApplication.query.filter_by(user_id=user.id).all()
    return my_leaves


def search(search_for):
    # find if the given word is in the dict
    categories = {
        "annual_leave": 'Annual Leave', "sick_leave": 'Sick Leave', "family_leave": 'Family Leave',
        "unpaid_leave": 'Unpaid Leave', "study_leave": 'Study Leave', "compensation_leave": 'Compensation Leave',
        "other_leave": 'Other Leave'
    }
    for k, v in categories.items():
        if search_for == v:
            return k


# the covid questionnaire
@automation.route("/covid-question", methods=['GET', 'POST'])
@login_required
def covid_questionnaire():
    # if the logged in user has completed the questionnaire for the day
    if covid_questionnaire_completed(current_user.id):
        return redirect(url_for('home'))
    else:
        # the current user has not completed the questionnaire for the day
        form = CovidQuestionsForm()
        if form.validate_on_submit():
            submitted_covid_questionnaire = CovidQuestionnaire(user_id=current_user.id,
                                                               temperature=int(float(form.temperature.data)),
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
            return redirect(url_for('main.home'))
    return render_template('covid_questions.html', form=form)


def covid_questionnaire_completed(user_id):
    # queries the database to check if the user has completed the questionnaire today
    latest_questionnaire = CovidQuestionnaire.query.filter_by(user_id=user_id)
    todays_date = datetime.now().date()
    for i in latest_questionnaire:
        if todays_date == i.time_signed.date():
            return True
    return False


