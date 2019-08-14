#forms.py
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, underscores and dot')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', 'Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email have already registered.')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username have already registered.')

class EmailForm(Form):
    email = StringField('Please input your email', validators=[Required(), Length(1,64), Email()])
    submit = SubmitField('Commit')

class ResetpasswordForm(Form):
    password = PasswordField('New password', validators=[Required(), EqualTo('password2', 'Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset password')

