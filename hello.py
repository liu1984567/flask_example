from flask import Flask, render_template, session, url_for, flash
from flask import redirect
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import smtplib
from email.mime.text import MIMEText
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_SERVER_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<user %r>' % self.username

def send_mail(to, subject, template, **kwargs):
    from_email = app.config['MAIL_USERNAME']
    msg = MIMEText(render_template(template + '.txt', **kwargs))
    msg['From'] = from_email
    msg['To'] = to 
    msg['Subject'] = app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject
    email_server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_SERVER_PORT'])
    email_server.set_debuglevel(1)
    email_server.login(from_email, app.config['MAIL_PASSWORD'])
    email_server.sendmail(from_email, [to], msg.as_string())
    email_server.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            newuser = User(username=form.name.data)
            db.session.add(newuser)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                print('New user %s, send a email to admin' % newuser.username)
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=newuser)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known'))

#/user/liudonghao
@app.route('/user/<name>')
def user(name):
    print('hello /user/%s' % name)
    return render_template('user.html', name=name)
    #return '<h1>Hello, %s</h1>' % name

@app.route('/redirect/bing')
def jump_bing():
    return redirect('https://cn.bing.com/')

@app.route('/test/')
def test():
    #moment.include_moment()
    return '<h1>time: %s </h1>' % datetime.utcnow()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
