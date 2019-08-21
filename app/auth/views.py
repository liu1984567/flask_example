"""
    app.auth.views.py

    Implements all views in the app.
"""
from flask import render_template,redirect,url_for,flash,request,session
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_mail
from .. import logger
from .forms import LoginForm, RegistrationForm, ResetpasswordForm, EmailForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalidate email or password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    logger.info('Enter register')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        logger.info('New user id %d', user.id)
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm your account', 'auth/email/confirm', user=user,token=token)
        str_confirmlink = url_for('auth.confirm', token=token, _external=True)
        logger.info('confirm link: ' + str_confirmlink)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    #logger.info('Enter confirm: token {}' % (token))
    if (current_user.confirmed):
        return redirect(url_for('main.index'))
    if (current_user.confirm(token)):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/sendconfirmation')
def sendconfirmation():
    user = current_user
    token = user.generate_confirmation_token()
    send_mail(user.email, 'Confirm your account', 'auth/email/confirm', user=user,token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static' : 
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/resetpassword', methods=['GET', 'POST'])
def send_resetpassword():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_resetpwd_token()
            send_mail(user.email, 'Reset your password', 'auth/email/resetpwd', user=user,token=token)
            session['email'] = form.email.data
            flash('A reset password email has been sent to you by email.')
            return redirect(url_for('auth.login'))
        flash('The email has not been registered!')
    return render_template('auth/inputemail.html', form=form)

@auth.route('/resetpwd/<token>')
def start_resetpassword(token):
    email = session.get('email')
    if email:
        user = User.query.filter_by(email=email).first()
        if user and user.check_resetpwd_token(token):
            #form = ResetpasswordForm()
            #return render_template('auth/resetpwd.html', form=form)
            return redirect(url_for('auth.resetpwd'))
        flash('Email %s has not been registered or the token has been expired!' % (email))
    return redirect(url_for('auth.login'))

@auth.route('/resetpwd', methods=['GET', 'POST'])
def resetpwd():
    form = ResetpasswordForm()
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    logger.info('resetpwd user %s' % user.username)
    if user and form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been update, please login with new password')
        return redirect(url_for('auth.login'))
    return render_template('auth/resetpwd.html', form=form)

@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
