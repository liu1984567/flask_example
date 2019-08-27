#forms.py
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email, Regexp
from wtforms.widgets.core import TextArea
from flask_pagedown.fields import PageDownField
from ..models import User, Role

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    name = StringField('Real name?', validators=[Length(0,64)])
    location = StringField('Location?', validators=[Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, underscores and dot')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name?', validators=[Length(0,64)])
    location = StringField('Location?', validators=[Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.user = user
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
    
    def validate_email(self, field):
        if self.user.email != self.email.data and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email have already registered.')
    def validate_username(self, field):
        if self.user.username != self.username.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username have already registered.')

class PostForm(Form):
    #body = TextAreaField('What is on your mind?')
    body = PageDownField('What is on your mind?')
    submit = SubmitField('Submit')

class PostFormEx(Form):
    title = StringField(u'title', validators=[Required()])
    body = StringField(u'Text', widget=TextArea())
