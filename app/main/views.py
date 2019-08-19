"""
    app.main.views.py

    Implements all views in the app.
"""
from flask import redirect, render_template, session, url_for, current_app
from flask_login import login_required 
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User, RolePermissionCode
from ..email import send_mail
from ..decorators import permission_required, admin_required


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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

@main.route('/moderator')
@login_required
@permission_required(RolePermissionCode.MODERATOR)
def for_moderator_only():
    return 'For comment moderators!'

@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For administrators!'
