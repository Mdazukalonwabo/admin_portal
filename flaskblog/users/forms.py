from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   # to enable upload of files
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    """
    Registration form for a new user that
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Number', validators=[DataRequired(), Length(min=10, max=13)])
    id_number = StringField('ID Number', validators=[DataRequired(), Length(min=13, max=13)])
    type = StringField('Role', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please Choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already exist. Please try logging in.")

    def validate_id_number(self, id_number):
        user = User.query.filter_by(ID_number=id_number.data).first()
        if user:
            raise ValidationError("This id number already exist")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])

    phone_number = StringField('Contact Number', validators=[Length(min=10, max=13)])
    id_number = StringField('ID Number', validators=[Length(min=13, max=13)])

    next_of_kin = StringField('Next of kin', validators=[DataRequired(), Length(min=2, max=20)])
    next_of_kin_phone_number = StringField('Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField(label="Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please Choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email already exist. Please try logging in.")


class ActiveAccountForm(FlaskForm):
    active = BooleanField("Activate Account")
    submit = SubmitField("Activate")
