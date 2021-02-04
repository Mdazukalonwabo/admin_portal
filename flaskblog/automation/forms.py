from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   # to enable upload of files
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class CovidQuestionsForm(FlaskForm):
    """
    Covid-19 questionnaire that will be displayed to the user to fill in
    """
    temperature = StringField('Temperature', validators=[DataRequired()]) #FloatField
    Shortness_of_breath = RadioField('Shortness of Breath', choices=[('TRUE', 'Yes'), ('FALSE', 'No')])
    loss_of_taste_or_smell = RadioField('Loss of Taste or Smell', choices=[('TRUE', 'Yes'), ('FALSE', 'No')])
    sore_throat = RadioField('Sore Throat', choices=[('TRUE', 'Yes'), ('FALSE', 'No')])
    contact_with_Covid = RadioField('In contact with someone that has Covid-19', choices=[('TRUE', 'Yes'),
                                                                                          ('FALSE', 'No')])
    nasal_congestion = RadioField('Nasal Congestion', choices=[('TRUE', 'Yes'), ('FALSE', 'No')])
    diarrhea = RadioField('Diarrhea', choices=[('TRUE', 'Yes'), ('FALSE', 'No')])
    nausea = RadioField('Nausea', choices=[('TRUE', 'Yes'), ('FALSE', 'No')])
    submit = SubmitField("Submit")


class LeaveRequestForm(FlaskForm):
    start_date = DateField("From", format='%Y-%m-%d')
    end_date = DateField("to")
    certificate = FileField("Upload Doctor's Certificate", validators=[FileAllowed(['jpg', 'png'])])
    authorisation = BooleanField("Pre Authorised")
    message = StringField('Please specify')     # validators=[DataRequired()])
    leave_type = StringField('Leave type')
    submit = SubmitField("Request Leave")



