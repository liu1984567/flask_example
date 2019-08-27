"""
    app.main.views.py

    Implements all views in the app.
"""
from flask import redirect, render_template, session, url_for, current_app, request
from flask import abort
from flask_login import login_required, current_user
from datetime import datetime
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, PostFormEx
from .. import db
from ..models import User, RolePermissionCode, Permission, Post
from ..email import send_mail
from ..decorators import permission_required, admin_required
from .. import logger


@main.route('/', methods=['GET', 'POST'])
def index():
    #form = PostForm()
    form = PostFormEx()
    if current_user.can(Permission.WRITE_ARTICLES ) and form.validate_on_submit():
        post = Post(body=form.body.data, author_id=current_user.id)
        db.session.add(post)
        return redirect(url_for('main.index'))
    #posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

#/user/liudonghao
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = current_user
    form = EditProfileForm()
    logger.info('edit_profile name %s'% form.name.data)
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
    logger.info('user name %s' % user.name)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data
        logger.info('form name %s' % form.name.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
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
