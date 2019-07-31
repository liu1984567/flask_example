"""
    app.main.views.py

    Implements all views in the app.
"""
from flask import redirect, render_template, session, url_for, flash
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            newuser = User(username=form.name.data)
            db.session.add(newuser)
            session['known'] = False
            #if app.config['FLASKY_ADMIN']:
            #    print('New user %s, send a email to admin' % newuser.username)
            #    send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=newuser)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known'))

#/user/liudonghao
@main.route('/user/<name>')
def user(name):
    print('hello /user/%s' % name)
    return render_template('user.html', name=name)
    #return '<h1>Hello, %s</h1>' % name

@main.route('/redirect/bing')
def jump_bing():
    return redirect('https://cn.bing.com/')

@main.route('/test/')
def test():
    #moment.include_moment()
    return '<h1>time: %s </h1>' % datetime.utcnow()

