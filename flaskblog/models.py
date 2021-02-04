from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
import enum


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # extra info about the user
    ID_number = db.Column(db.String(13), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    next_of_kin = db.Column(db.String(20))
    next_of_kin_phone_number = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(120))
    active = db.Column(db.Boolean, nullable=False, default=False)

    #   creating a one-to-one relationship to the Leave class
    Leaves = db.relationship("LeaveApplication", backref='leave', lazy=True)

    #   creating a one-to-one relationship to the CovidQuestionnaire class
    covid_question = db.relationship("CovidQuestionnaire", backref='covid', lazy=True)

    def __repr__(self):
        return f"User '{self.username}', '{self.email}', '{self.image_file}'"

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()


# Covid Questionnaire
class CovidQuestionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    Shortness_of_breath = db.Column(db.Boolean, nullable=False)
    sore_throat = db.Column(db.Boolean, nullable=False)
    loss_of_taste_or_smell = db.Column(db.Boolean, nullable=False)
    contact_with_Covid = db.Column(db.Boolean, nullable=False)
    nasal_congestion = db.Column(db.Boolean, nullable=False)
    diarrhea = db.Column(db.Boolean, nullable=False)
    nausea = db.Column(db.Boolean, nullable=False)
    time_signed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return f"{self.temperature} on the {self.time_signed}"


class LeaveType(enum.Enum):
    annual_leave = 'Annual Leave',
    sick_leave = 'Sick Leave',
    family_leave = 'Family Leave',
    unpaid_leave = 'Unpaid Leave',
    study_leave = 'Study Leave',
    compensation_leave = 'Compensation Leave',
    other_leave = 'Other Leave'


# Leave Application
class LeaveApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Enum(LeaveType), nullable=False)
    pre_authorisation = db.Column(db.Boolean, nullable=False, default=False)
    personal_message = db.Column(db.Text, nullable=False)
    leave_date_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leave_date_to = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    approved = db.Column(db.Boolean, nullable=False, default=False)

    def __str__(self):
        return f"{self.category} ---- {self.leave_date_from} - {self.leave_date_to}"
