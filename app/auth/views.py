"""
    app.auth.views.py

    Implements all views in the app.
"""
from flask import render_template,redirect,url_for,flash
from flask_login import login_required
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            return redirect(url_for('main.index'))
        flash('Invalidate email or password')
    return render_template('auth/login.html', form=form)

@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
