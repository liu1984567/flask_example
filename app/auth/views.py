"""
    app.auth.views.py

    Implements all views in the app.
"""
from flask import render_template
from . import auth
from .. import db
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('/auth/login.html')
