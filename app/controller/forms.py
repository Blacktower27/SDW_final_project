import wtforms
from wtforms.validators import Length, Email, EqualTo, DataRequired, Regexp
from app.models.uicer import Uicer
from flask_wtf.file import FileField, FileRequired
from flask_wtf import FlaskForm

class AvatarForm(FlaskForm):
    avatar = FileField(validators=[FileRequired()])

class RegistForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=1, max=20, message='User name format error')])
    email = wtforms.StringField(validators=[DataRequired(),Regexp('^([a-z]\d{9}|[a-z]\d{9}@uic\.edu\.cn)$', message='Email format error')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password format error')])
    c_password = wtforms.StringField(validators=[ EqualTo('password')])

    def validate_email(self, field):
        email = field.data
        user = Uicer.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="The email had been used")

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[DataRequired(),Regexp('^([a-z]\d{9}|[a-z]\d{9}@uic\.edu\.cn)$', message='Email format error')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password format error')])

class PasswordFrom(wtforms.Form):
    new_password = wtforms.StringField(validators=[Length(min=6, max=20, message='Password format error')])

# class KpFrom(wtforms.form):
#     programName= wtforms.StringField()
#     university = wtforms.StringField()
#     courseNameList = wtforms.StringField()
#
#     def validate_programName(self, field):