"""
    app.main.views.py

    Implements all views in the app.
"""
from flask import redirect, render_template, session, url_for, current_app
from flask import abort
from flask_login import login_required, current_user
from datetime import datetime
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, RolePermissionCode
from ..email import send_mail
from ..decorators import permission_required, admin_required
from .. import logger


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#/user/liudonghao
@main.route('/user/<username>')
def user(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    return render_template('user.html', user=u)

@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = current_user
    form = EditProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        return redirect(url_for('main.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('editprofile.html', form=form)

@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        return redirect(url_for('main.user', username=user.username))
    return render_template('editprofile.html', form=form)

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
